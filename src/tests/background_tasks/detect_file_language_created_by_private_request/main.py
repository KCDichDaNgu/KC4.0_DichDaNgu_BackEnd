from datetime import datetime

from core.utils.common import chunk_arr
import pymongo

from typing import List
from uuid import UUID

from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.task import (
    LanguageDetectionTaskNameEnum, 
    LanguageDetectionTaskStepEnum, 
    StepStatusEnum
)

from modules.language_detection_request.database.language_detection_request.repository import LanguageDetectionRequestRepository
from modules.language_detection_request.database.language_detection_request_result.repository import LanguageDetectionRequestResultRepository
from modules.language_detection_request.database.language_detection_history.repository import LanguageDetectionHistoryRepository
from modules.system_setting.database.repository import SystemSettingRepository
from modules.background_tasks.detect_file_language_created_by_private_request.main import read_task_result, mark_invalid_tasks, execute_in_batch

import asyncio
import pandas

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

language_detection_request_repository = LanguageDetectionRequestRepository()
language_detection_request_result_repository = LanguageDetectionRequestResultRepository()
language_detection_history = LanguageDetectionHistoryRepository()
system_setting_repository = SystemSettingRepository()

df = pandas.read_csv('src/tests/background_tasks/detect_file_language_created_by_private_request/sample_data/detect_file_language_data.csv')

async def get_input_data():
    system_setting = await system_setting_repository.find_one({})    
    ALLOWED_CONCURRENT_REQUEST = system_setting.props.language_detection_api_allowed_concurrent_req
    
    if ALLOWED_CONCURRENT_REQUEST <= 0: return
    
    tasks = await language_detection_request_repository.find_many(
        params=dict(
            current_step=LanguageDetectionTaskStepEnum.detecting_language.value,
            step_status=StepStatusEnum.not_yet_processed.value
        ),
        limit=1,
        order_by=[('created_at', pymongo.ASCENDING)]
    )
        
    if not tasks or not (tasks[0].props.task_name == LanguageDetectionTaskNameEnum.private_file_language_detection.value and \
        tasks[0].props.current_step == LanguageDetectionTaskStepEnum.detecting_language.value and \
        tasks[0].props.step_status in [StepStatusEnum.not_yet_processed.value]): 
        print ('Invalid State')
        return 
    
    try:
        
        tasks = await language_detection_request_repository.find_many(
            params=dict(
                task_name=LanguageDetectionTaskNameEnum.private_file_language_detection.value,
                current_step=LanguageDetectionTaskStepEnum.detecting_language.value,
                step_status=StepStatusEnum.not_yet_processed.value
            ),
            limit=ALLOWED_CONCURRENT_REQUEST
        )

        tasks_id = list(map(lambda task: task.id.value, tasks))

        if len(tasks_id) == 0: 
            print('Invalid task detect_file_language_created_by_private_request')
            return

        tasks_result_and_trans_history_req = [
            language_detection_request_result_repository.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    },
                    step=LanguageDetectionTaskStepEnum.detecting_language.value
                )
            ),
            language_detection_history.find_many(
                params=dict(
                    task_id={
                        '$in': list(map(lambda t: UUID(t), tasks_id))
                    }
                )
            )
        ]

        tasks_result, language_detections_history = await asyncio.gather(*tasks_result_and_trans_history_req)

        return tasks, tasks_result, language_detections_history


    except Exception as e:
        print(e)


async def test_read_task_result():
    print ('----------------Detect file language created by private request: Test Read Task Result----------------')

    tasks, tasks_result, language_detections_history = await get_input_data()

    valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
        tasks_result,
        tasks,
        language_detections_history
    )

    print ('---------------- Valid Task: ', valid_tasks_mapper)
    print ('---------------- Invalid Task Comparision: ', list(invalid_tasks_mapper)[0] == df.iloc[-1,:][0])


async def test_mark_invalid_tasks():
    print ('----------------Detect file language created by private request: Test Mark Invalid Tasks----------------')

    tasks, tasks_result, language_detections_history = await get_input_data()

    _, invalid_tasks_mapper = await read_task_result(
        tasks_result,
        tasks,
        language_detections_history
    )
    

    result = await mark_invalid_tasks(invalid_tasks_mapper)

    print ('---------------- Status of Task: ', result[1].props.status == 'cancelled')

async def test_execute_in_batch(allowed_concurrent_request):
    print ('----------------Detect file language created by private request: Test Execute In Batch----------------')

    tasks, tasks_result, language_detections_history = await get_input_data()

    valid_tasks_mapper, _ = await read_task_result(
        tasks_result,
        tasks,
        language_detections_history
    )

    valid_tasks_id = list(map(lambda t: t.id.value, tasks))
    chunked_tasks_id = list(chunk_arr(valid_tasks_id, allowed_concurrent_request))

    for task_id in chunked_tasks_id:
        await execute_in_batch (valid_tasks_mapper, task_id, allowed_concurrent_request)

    print ('---------------- The execute_in_batch runs well')

    

async def test_all():
    system_setting = await system_setting_repository.find_one({})
    ALLOWED_CONCURRENT_REQUEST = system_setting.props.language_detection_api_allowed_concurrent_req

    # await test_read_task_result()
    # await test_mark_invalid_tasks()
    await test_execute_in_batch(ALLOWED_CONCURRENT_REQUEST)
    # await test_main()
