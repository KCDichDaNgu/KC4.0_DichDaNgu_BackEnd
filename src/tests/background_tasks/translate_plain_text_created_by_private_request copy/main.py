# from email.mime import image
import random
from datetime import datetime
from sqlite3 import Date
from typing import Union
from uuid import UUID
from core.utils.common import chunk_arr

from nltk import data
from typing import List

from core.value_objects.id import ID

import pandas
import json
from tqdm import asyncio
from umongo.frameworks import pymongo

from core import Entity

from infrastructure.configs.task import StepStatusEnum, CreatorTypeEnum
from infrastructure.configs.translation_history import TranslationHistoryStatus
from infrastructure.configs.translation_task import TranslationTaskNameEnum, TranslationTaskStepEnum
from modules.background_tasks.translate_plain_text_created_by_private_request.translate_content.main import (
    read_task_result, mark_invalid_tasks, execute_in_batch, main)
from modules.system_setting.database.repository import SystemSettingRepository
from modules.task.domain.entities.task_result import TaskResultEntity, TaskResultProps
from modules.translation_request.commands.create_plain_text_translation_request.command import \
    CreatePlainTextTranslationRequestCommand
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository
from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
from modules.translation_request.database.translation_request_result import TranslationRequestResultRepository
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity, \
    TranslationHistoryProps
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, \
    TranslationRequestProps
from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultEntity, \
    TranslationRequestResultProps
import pandas

translation_request_repository = TranslationRequestRepository()
translation_request_result_repository = TranslationRequestResultRepository()
translation_history_repository = TranslationHistoryRepository()
system_setting_repository = SystemSettingRepository()


async def test_read_task_result():
    df = read_data()
    # df = pandas.read_csv('src/tests/background_tasks/delete_invalid_file/sample_data/task_file_data.csv')
    print("===>>>>>>> Test read_task_result <<<<<<<<<<<<===")
    print("TEST 1")
    try:
        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result([], [], [])
        print("=== Test read_task_result in testcase 1: TRUE  ===")
    except Exception as e:
        print(e)
        print("=== Test read_task_result in testcase 1: FALSE ===")

    print("TEST 2")

    try:
        # print("task init: ")
        for x in range(5):
            print("Test case " + x + ": \n")
            data = df.get(1)
            new_request = create_new_request(df.get(random.randint(0, 4)))
            tran = TranslationRequestResultEntity(
                TranslationRequestResultProps(
                    task_id=new_request.id,
                    step=new_request.props.current_step,
                )
            )
            tasks = [tran]

            # print("task_res init: ")
            new_request_res = create_new_request(df.get(random.randint(0, 4)))
            task_res = TranslationRequestResultEntity(
                TranslationRequestResultProps(
                    task_id=new_request_res.id,
                    step=new_request_res.props.current_step
                )
            )
            # print(task_res)
            tasks_result = [task_res]

            # print("history init ")
            new_request_his = create_new_request(df.get(random.randint(0, 4)))
            tran_history = TranslationHistoryEntity(
                TranslationHistoryProps(
                    creator_id=new_request_his.props.creator_id,
                    task_id=new_request_his.id,
                    translation_type=new_request_his.props.task_name,
                    status=TranslationHistoryStatus.translating.value,
                    file_path=data.file_path
                )
            )
            translations_history = [tran_history]
            print("INIT ARGUMENT SUCCESS")

            valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
                tasks=tasks,
                tasks_result=tasks_result,
                translations_history=translations_history
            )
    except Exception as e:
        print(e)
        print("=== Test read_task_result: FALSE ===")


async def test_mark_invalid_tasks():
    print("===>>>>>>> Test mark_invalid_tasks <<<<<<<<<<<<===")

    print("TEST1: ")
    try:
        print("INIT ARGUMENT SUCCESS")
        invalid_tasks_mapper = {}
        await mark_invalid_tasks(invalid_tasks_mapper)
        print("=== Test mark_invalid_tasks in testcase 1: TRUE ===")
    except Exception as e:
        print(e)
        print("=== Test mark_invalid_tasks in testcase 1: FALSE ===")

    print("TEST 2: ")
    try:
        df = read_data()
        for x in df:
            # print("task init: ")
            new_request = create_new_request(df.get(random.randint(0, 4)))
            tran = TranslationRequestResultEntity(
                TranslationRequestResultProps(
                    task_id=new_request.id,
                    step=new_request.props.current_step,
                )
            )
            tasks = [tran]

            # print("task_res init: ")
            new_request_res = create_new_request(df.get(random.randint(0, 4)))
            task_res = TranslationRequestResultEntity(
                TranslationRequestResultProps(
                    task_id=new_request_res.id,
                    step=new_request_res.props.current_step
                )
            )
            # print(task_res)
            tasks_result = [task_res]

            # print("history init ")
            new_request_his = create_new_request(df.get(random.randint(0, 4)))
            tran_history = TranslationHistoryEntity(
                TranslationHistoryProps(
                    creator_id=new_request_his.props.creator_id,
                    task_id=new_request_his.id,
                    translation_type=new_request_his.props.task_name,
                    status=TranslationHistoryStatus.translating.value,
                    file_path="1648110429829__89aa81e5-6dca-4589-afc4-af2f56d9cb9f.json"
                )
            )
            translations_history = [tran_history]

            print("INIT ARGUMENT SUCCESS")
            invalid_tasks_mapper = {0: {
                'task_result': tasks_result,
                'trans_history': translations_history,
                'task': tasks
            }}
            await mark_invalid_tasks(invalid_tasks_mapper)
            print("=== Test mark_invalid_tasks in testcase " + df.index(x) + ": TRUE ===")
    except Exception as e:
        print(e)
        print("=== Test mark_invalid_tasks in testcase 2: FALSE ===")


async def test_execute_in_batch():
    print("===>>>>>>> Test execute_in_batch <<<<<<<<<<<<===")
    from modules.system_setting.database.repository import SystemSettingRepository

    system_setting_repository = SystemSettingRepository()
    system_setting = await system_setting_repository.find_one({})

    ALLOWED_CONCURRENT_REQUEST = system_setting.props.translation_api_allowed_concurrent_req

    print("TEST 1: ")
    try:
        print("INIT ARGUMENT SUCCESS")
        valid_tasks_mapper = []
        await execute_in_batch(valid_tasks_mapper, [], ALLOWED_CONCURRENT_REQUEST)
        print("Test execute_in_batch in testcase 1: TRUE")
    except Exception as e:
        print(e)
        print("Test execute_in_batch in testcase 1: FALSE")

    print("TEST 2: ")
    try:
        await execute_in_batch([], [], None)
        print("Test execute_in_batch in test case 2: TRUE")
    except Exception as e:
        print(e)
        print("Test execute_in_batch in test case 2: FALSE")

    # try:
    #     tasks: List[TranslationRequestEntity]
    #     tasks_result: List[TranslationRequestResultEntity]
    #     translations_history: List[TranslationHistoryEntity]

    # except Exception as e:
    #     print(e)
    #     return


async def test_main():
    print("=== Test main ===")
    read_data()
    try:
        main()
        print('Test translate_plain_text_created_by_private_request TRUE')
    except Exception as e:
        print(e)
        print('Test translate_plain_text_created_by_private_request FALSE')


def read_data():
    df = pandas.read_csv('data.csv',
                         )
    print(df)

def create_new_request(data):
    return TranslationRequestEntity(
            TranslationRequestProps(
            creator_id=data.creator_id,
            creator_type=data.creator_type,
            task_name=data.task_name,
            step_status=data.step_status,
            current_step=data.current_step,
            create_at=Date(2022, 3, 24),
            _cls=data._cls
        )
    )
