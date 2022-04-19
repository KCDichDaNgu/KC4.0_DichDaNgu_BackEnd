# from email.mime import image
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
from modules.background_tasks.translate_plain_text_created_by_public_request.translate_content.main import (
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

translation_request_repository = TranslationRequestRepository()
translation_request_result_repository = TranslationRequestResultRepository()
translation_history_repository = TranslationHistoryRepository()
system_setting_repository = SystemSettingRepository()

print ("Test translate_plain_text_created_by_private_request")


async def test_read_task_result():

    # df = pandas.read_csv('src/tests/background_tasks/delete_invalid_file/sample_data/task_file_data.csv')
    print("----Test read_task_result----")
    print("TEST CASE 1")
    try:
        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result([], [], [])
        print("---- Test read_task_result in testcase 1: TRUE  ----")
    except Exception as e:
        print(e)
        print("---- Test read_task_result in testcase 1: FALSE ----")

    print("TEST 2")
    try:
        # print("task init: ")
        new_request = TranslationRequestEntity(
            TranslationRequestProps(
                creator_id=ID("660c1f23-6d26-41e8-a5dd-736c44248d0e"),
                creator_type="end_user",
                task_name='public_plain_text_translation',
                step_status="closed",
                current_step="detecting_language",
                create_at=Date(2022, 3, 31),
                _cls="LanguageDetectionRequestOrmEntity"
            )
        )
        tran = TranslationRequestResultEntity(
            TranslationRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step,
            )
        )
        tasks = [tran]

        # print("task_res init: ")
        new_request_res = TranslationRequestEntity(
            TranslationRequestProps(
                id=ID("660c1f23-6d26-41e8-a5dd-736c44248d0e"),
                creator_id=ID("377b5a56-51bd-40e7-8b52-73060e5f8c32"),
                creator_type="end_user",
                task_name='public_plain_text_translation',
                step_status="closed",
                current_step="detecting_language",
                create_at=Date(2022, 3, 31),
                update_at=Date(2022, 3, 31),
                _cls="LanguageDetectionRequestOrmEntity",
                file_path="1648110413183__660c1f23-6d26-41e8-a5dd-736c44248d0e.json"
            )
        )
        task_res = TranslationRequestResultEntity(
            TranslationRequestResultProps(
                task_id=new_request_res.id,
                step=new_request_res.props.current_step
            )
        )
        # print(task_res)
        tasks_result = [task_res]

        # print("history init ")
        new_request_his = TranslationRequestEntity(
            TranslationRequestProps(
                creator_id=ID("76b76d60-2682-4c53-b092-c8262a353dba"),
                creator_type=CreatorTypeEnum.end_user.value,
                task_name=TranslationTaskNameEnum.public_plain_text_translation.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=TranslationTaskStepEnum.detecting_language.value
            )
        )
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

        valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
            tasks=tasks,
            tasks_result=tasks_result,
            translations_history=translations_history
        )
        print("---- Test read_task_result: TRUE ----")
        # print("---- VALID TASKS MAPPER ----\n")
        # print(valid_tasks_mapper + "\n")
        # print("---- INVALID TASKS MAPPER ----\n")
        # print(invalid_tasks_mapper)
        # print("---- Test read_task_result: TRUE  ----")
    except Exception as e:
        print(e)
        print("---- Test read_task_result: FALSE ----")


async def test_mark_invalid_tasks():
    print("---->>>>>>> Test mark_invalid_tasks <<<<<<<<<<<<----")

    print("TEST1: ")
    try:
        print("INIT ARGUMENT SUCCESS")
        invalid_tasks_mapper = {}
        await mark_invalid_tasks(invalid_tasks_mapper)
        print("---- Test mark_invalid_tasks in testcase 1: TRUE ----")
    except Exception as e:
        print(e)
        print("---- Test mark_invalid_tasks in testcase 1: FALSE ----")

    print("TEST 2: ")
    try:
        # print("task init: ")
        new_request = TranslationRequestEntity(
            TranslationRequestProps(
                creator_id=ID("660c1f23-6d26-41e8-a5dd-736c44248d0e"),
                creator_type="end_user",
                task_name='public_plain_text_translation',
                step_status="closed",
                current_step="detecting_language",
                create_at=Date(2022, 3, 31),
                _cls="LanguageDetectionRequestOrmEntity"
            )
        )
        tran = TranslationRequestResultEntity(
            TranslationRequestResultProps(
                task_id=new_request.id,
                step=new_request.props.current_step,
            )
        )
        tasks = [tran]

        # print("task_res init: ")
        new_request_res = TranslationRequestEntity(
            TranslationRequestProps(
                id=ID("660c1f23-6d26-41e8-a5dd-736c44248d0e"),
                creator_id=ID("377b5a56-51bd-40e7-8b52-73060e5f8c32"),
                creator_type="end_user",
                task_name='public_plain_text_translation',
                step_status="closed",
                current_step="detecting_language",
                create_at=Date(2022, 3, 31),
                update_at=Date(2022, 3, 31),
                _cls="LanguageDetectionRequestOrmEntity",
                file_path="1648110413183__660c1f23-6d26-41e8-a5dd-736c44248d0e.json"
            )
        )
        task_res = TranslationRequestResultEntity(
            TranslationRequestResultProps(
                task_id=new_request_res.id,
                step=new_request_res.props.current_step
            )
        )
        # print(task_res)
        tasks_result = [task_res]

        # print("history init ")
        new_request_his = TranslationRequestEntity(
            TranslationRequestProps(
                creator_id=ID("76b76d60-2682-4c53-b092-c8262a353dba"),
                creator_type=CreatorTypeEnum.end_user.value,
                task_name=TranslationTaskNameEnum.public_plain_text_translation.value,
                step_status=StepStatusEnum.not_yet_processed.value,
                current_step=TranslationTaskStepEnum.detecting_language.value
            )
        )
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
        print("---- Test mark_invalid_tasks in testcase 1: TRUE ----")
    except Exception as e:
        print(e)
        print("---- Test mark_invalid_tasks in testcase 2: FALSE ----")


async def test_execute_in_batch():
    print("---->>>>>>> Test execute_in_batch <<<<<<<<<<<<----")
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
    print("---- Test main ----")
    await main()
    try:
        await main()
        print('Test translate_plain_text_created_by_public_request TRUE')
    except Exception as e:
        print(e)
        print('Test translate_plain_text_created_by_public_request FALSE')
