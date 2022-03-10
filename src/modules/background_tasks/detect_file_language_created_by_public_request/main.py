from datetime import datetime

from docx.api import Document
from core.utils.file import get_presentation_full_text, get_worksheet_full_text
from infrastructure.configs.message import MESSAGES
from infrastructure.configs.language_detection_task import FileLanguageDetectionTask_LangUnknownResultFileSchemaV1, FileLanguageDetectionTask_LanguageDetectionClosedResultFileSchemaV1, FileLanguageDetectionTask_LanguageDetectionCompletedResultFileSchemaV1, LanguageDetectionTask_LanguageDetectionClosedResultFileSchemaV1
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.language_detection_history import LanguageDetectionHistoryStatus
from core.utils.common import chunk_arr
import pymongo

from typing import List
from uuid import UUID

from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.task import (
    LanguageDetectionTask_LangUnknownResultFileSchemaV1, 
    LanguageDetectionTask_LanguageDetectionCompletedResultFileSchemaV1,
    LanguageDetectionTaskNameEnum, 
    LanguageDetectionTaskStepEnum, 
    StepStatusEnum
)

from infrastructure.adapters.language_detector.main import LanguageDetector

from modules.language_detection_request.database.language_detection_request.repository import LanguageDetectionRequestRepository, LanguageDetectionRequestEntity
from modules.language_detection_request.database.language_detection_request_result.repository import LanguageDetectionRequestResultRepository, LanguageDetectionRequestResultEntity
from modules.language_detection_request.database.language_detection_history.repository import LanguageDetectionHistoryRepository, LanguageDetectionHistoryEntity
from modules.system_setting.database.repository import SystemSettingRepository

import asyncio
import aiohttp

from infrastructure.adapters.logger import Logger

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

language_detection_request_repository = LanguageDetectionRequestRepository()
language_detection_request_result_repository = LanguageDetectionRequestResultRepository()
language_detection_history = LanguageDetectionHistoryRepository()
system_setting_repository = SystemSettingRepository()

languageDetector = LanguageDetector()

logger = Logger('Task: detect_file_language_created_by_public_request')

async def read_task_result(
    tasks_result: List[LanguageDetectionRequestResultEntity], 
    tasks: List[LanguageDetectionRequestEntity],
    language_detections_history: List[LanguageDetectionHistoryEntity]
):
    
    valid_tasks_mapper = {}

    task_id_1 = list(map(lambda t: t.id.value, tasks))
    task_id_2 = list(map(lambda ts: ts.props.task_id.value, tasks_result))
    task_id_3 = list(map(lambda th: th.props.task_id.value, language_detections_history))

    intersection_tasks_id = list(set(task_id_1) & set(task_id_2) & set(task_id_3))
    
    for task_id in intersection_tasks_id:

        task = list(filter(lambda ts: ts.id.value == task_id, tasks))[0]
        task_result = list(filter(lambda ts: ts.props.task_id.value == task_id, tasks_result))[0]
        trans_history = list(filter(lambda ts: ts.props.task_id.value == task_id, language_detections_history))[0]

        try: 
            data = await task_result.read_data_from_file()
            
            if data['status'] == FileLanguageDetectionTask_LangUnknownResultFileSchemaV1(
                source_file_full_path='',
                task_name=LanguageDetectionTaskNameEnum.public_file_language_detection.value,
                file_type=''
            ).status:

                valid_tasks_mapper[task_id] = {
                    'task_result_content': data,
                    'task_result': task_result,
                    'trans_history': trans_history,
                    'task': task
                }

        except Exception as e:
            logger.error(e)
            
            print(e)
            
    valid_tasks_id = valid_tasks_mapper.keys()

    invalid_tasks = list(filter(lambda t: t.id.value not in valid_tasks_id, tasks))

    invalid_tasks_id = list(map(lambda t: t.id.value, invalid_tasks))

    invalid_tasks_mapper = {}

    for task_id in invalid_tasks_id:

        task = list(filter(lambda ts: ts.id.value == task_id, tasks))[0]
        task_result = list(filter(lambda ts: ts.props.task_id.value == task_id, tasks_result))[0]
        trans_history = list(filter(lambda ts: ts.props.task_id.value == task_id, language_detections_history))[0]

        invalid_tasks_mapper[task_id] = {
            'task_result': task_result,
            'trans_history': trans_history,
            'task': task
        }

    return valid_tasks_mapper, invalid_tasks_mapper

async def mark_invalid_tasks(invalid_tasks_mapper):

    result = []
    
    async with db_instance.session() as session:
        async with session.start_transaction():

            update_request = []
            
            for task_id in invalid_tasks_mapper.keys():

                task_result = invalid_tasks_mapper[task_id]['task_result'],
                trans_history = invalid_tasks_mapper[task_id]['trans_history'],
                task = invalid_tasks_mapper[task_id]['task']

                if isinstance(task_result, tuple):
                    task_result = task_result[0]

                if isinstance(trans_history, tuple):
                    trans_history = trans_history[0]
                    
                update_request.append(
                    language_detection_request_repository.update(
                        task, 
                        dict(step_status=StepStatusEnum.cancelled.value),
                        conditions={}
                    )
                )
                
                update_request.append(
                    language_detection_history.update(
                        trans_history, 
                        dict(
                            status=LanguageDetectionHistoryStatus.cancelled.value
                        )
                    )
                )
                
            result = await asyncio.gather(*update_request)

    return result

async def main():
    
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
        
    if not tasks or not (tasks[0].props.task_name == LanguageDetectionTaskNameEnum.public_file_language_detection.value and \
        tasks[0].props.current_step == LanguageDetectionTaskStepEnum.detecting_language.value and \
        tasks[0].props.step_status in [StepStatusEnum.not_yet_processed.value]): return 

    logger.debug(
        msg=f'New task detect_file_language_created_by_public_request run in {datetime.now()}'
    )

    print(f'New task detect_file_language_created_by_public_request run in {datetime.now()}')
    
    try:
        
        tasks = await language_detection_request_repository.find_many(
            params=dict(
                task_name=LanguageDetectionTaskNameEnum.public_file_language_detection.value,
                current_step=LanguageDetectionTaskStepEnum.detecting_language.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                # expired_date={
                #     "$gt": datetime.now()
                # }
            ),
            limit=ALLOWED_CONCURRENT_REQUEST
        )

        tasks_id = list(map(lambda task: task.id.value, tasks))

        if len(tasks_id) == 0: 
            logger.debug(
                msg=f'An task detect_file_language_created_by_public_request end in {datetime.now()}\n'
            )

            print(f'An task detect_file_language_created_by_public_request end in {datetime.now()}\n')
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
    
        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
            tasks=tasks, 
            tasks_result=tasks_result,
            language_detections_history=language_detections_history
        )

        await mark_invalid_tasks(invalid_tasks_mapper)
        
        valid_tasks_id = list(map(lambda t: t.id.value, tasks))

        chunked_tasks_id = list(chunk_arr(valid_tasks_id, ALLOWED_CONCURRENT_REQUEST))

        for chunk in chunked_tasks_id:

            try:
            
                await execute_in_batch(valid_tasks_mapper, chunk, ALLOWED_CONCURRENT_REQUEST)
                
            except Exception as e:
                logger.error(e)
                
                print(e)

    except Exception as e:
        logger.error(e)
        
        print(e)

    logger.debug(
        msg=f'An task detect_file_language_created_by_public_request end in {datetime.now()}\n'
    )

    print(f'An task detect_file_language_created_by_public_request end in {datetime.now()}\n')
            

async def execute_in_batch(valid_tasks_mapper, tasks_id, allowed_concurrent_request):

    loop = asyncio.get_event_loop()

    connector = aiohttp.TCPConnector(limit=allowed_concurrent_request)

    async with aiohttp.ClientSession(connector=connector, loop=loop) as session:
        
        api_requests = []

        for task_id in tasks_id:
            task_result_content = valid_tasks_mapper[task_id]['task_result_content']
            source_file_full_path = task_result_content['source_file_full_path']
            file_type = task_result_content['file_type']
            source_text = ''
            
            try:
                if file_type == 'docx':
                    doc = Document(source_file_full_path)
                    
                    for paragraph in doc.paragraphs:
                        source_text = source_text + paragraph.text
                elif file_type == 'txt':
                    try:

                        original_file = open(source_file_full_path, mode='r',encoding="utf-16", errors="ignore")
                        source_text = original_file.read()

                    except Exception as e:
                        original_file = open(source_file_full_path, mode='r',encoding="utf-8", errors="ignore")
                        source_text = original_file.read()
                        
                elif file_type == 'pptx':
                    source_text = get_presentation_full_text(source_file_full_path)
                    
                elif file_type == 'xlsx':
                    source_text = get_worksheet_full_text(source_file_full_path)
                    
            except Exception as e:
                print(e)

            api_requests.append(
                languageDetector.detect(
                    text=source_text, 
                    session=session
                )
            )

        api_results = await asyncio.gather(*api_requests)
        
        async with db_instance.session() as session:

            async with session.start_transaction():
    
                update_request = []

                for task_id, api_result in zip(tasks_id, api_results):

                    task_result = valid_tasks_mapper[task_id]['task_result'],
                    trans_history = valid_tasks_mapper[task_id]['trans_history'],
                    task = valid_tasks_mapper[task_id]['task']
                    task_result_content = valid_tasks_mapper[task_id]['task_result_content']

                    if api_result.lang == LanguageEnum.unknown.value:

                        new_saved_content = FileLanguageDetectionTask_LanguageDetectionClosedResultFileSchemaV1(
                            source_file_full_path=task_result_content['source_file_full_path'],
                            source_lang=api_result.lang,
                            file_type=task_result_content['file_type'],
                            message=MESSAGES['content_language_is_not_supported'],
                            task_name=LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value
                        )

                        if isinstance(task_result, tuple):
                            task_result = task_result[0]

                        if isinstance(trans_history, tuple):
                            trans_history = trans_history[0]
                    
                        update_request.append(
                            language_detection_request_repository.update(
                                task, 
                                dict(
                                    step_status=StepStatusEnum.closed.value
                                )
                            )
                        )
                        
                        update_request.append(
                            language_detection_history.update(
                                trans_history, 
                                dict(
                                    status=LanguageDetectionHistoryStatus.closed.value
                                )
                            )
                        )

                        update_request.append(
                            task_result.save_request_result_to_file(
                                content=new_saved_content.json()
                            )
                        )

                    else:

                        new_saved_content = FileLanguageDetectionTask_LanguageDetectionCompletedResultFileSchemaV1(
                            source_file_full_path=task_result_content['source_file_full_path'],
                            source_lang=api_result.lang,
                            file_type=task_result_content['file_type'],
                            task_name=LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value
                        )

                        if isinstance(task_result, tuple):
                            task_result = task_result[0]

                        if isinstance(trans_history, tuple):
                            trans_history = trans_history[0]
                    
                        update_request.append(
                            language_detection_request_repository.update(
                                task, 
                                dict(
                                    step_status=StepStatusEnum.completed.value
                                )
                            )
                        )
                        
                        update_request.append(
                            language_detection_history.update(
                                trans_history, 
                                dict(
                                    status=LanguageDetectionHistoryStatus.detected.value
                                )
                            )
                        )

                        update_request.append(
                            task_result.save_request_result_to_file(
                                content=new_saved_content.json()
                            )
                        )

                await asyncio.gather(*update_request)
