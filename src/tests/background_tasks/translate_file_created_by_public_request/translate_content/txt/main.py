from core.utils.common import chunk_arr
from core.utils.document import check_if_paragraph_has_text, get_common_style
from core.utils.file import get_doc_paragraphs, get_full_path
from datetime import datetime
from docx import Document
from infrastructure.adapters.content_translator.main import ContentTranslator
from infrastructure.adapters.logger import Logger
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.task import TranslationTask_TranslationCompletedResultFileSchemaV1, TranslationTask_NotYetTranslatedResultFileSchemaV1, TranslationTaskNameEnum, TranslationTaskStepEnum, StepStatusEnum
from infrastructure.configs.translation_history import TranslationHistoryStatus
from infrastructure.configs.translation_task import RESULT_FILE_STATUS, AllowedFileTranslationExtensionEnum, FileTranslationTask_NotYetTranslatedResultFileSchemaV1, FileTranslationTask_TranslatingResultFileSchemaV1, FileTranslationTask_TranslationCompletedResultFileSchemaV1, get_file_translation_file_path, get_file_translation_target_file_name
from inspect import trace
from modules.background_tasks.translate_file_created_by_public_request.translate_content.txt.main import *
from modules.system_setting.database.repository import SystemSettingRepository
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository, TranslationHistoryEntity, TranslationHistoryProps
from modules.translation_request.database.translation_request.repository import TranslationRequestRepository, TranslationRequestEntity, TranslationRequestProps
from modules.translation_request.database.translation_request_result.repository import TranslationRequestResultRepository, TranslationRequestResultEntity, TranslationRequestResultProps
from typing import List
from uuid import UUID
import aiohttp
import asyncio
import io
import json
import pickle
import pymongo
import random
import traceback

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

LIMIT_NUM_CHAR_TRANSLATE_REQUEST = 3000

translation_request_repository = TranslationRequestRepository()
translation_request_result_repository = TranslationRequestResultRepository()
translation_history_repository = TranslationHistoryRepository()
system_setting_repository = SystemSettingRepository()

contentTranslator = ContentTranslator()

logger = Logger(
    'Task: translate_file_created_by_public_request.translate_content.txt'
)


async def test_read_task_result():
    print('=====================test_read_task_result=====================')
    seed = 31415
    random.seed(seed)
    print(f'Random seed is {seed}')

    try:
        tasks: List[TranslationRequestEntity]
        tasks_result: List[TranslationRequestResultEntity]
        translations_history: List[TranslationHistoryEntity]

        # Get task from database
        tasks = await translation_request_repository.find_many(
            params={
                'task_name': {
                    '$in': [TranslationTaskNameEnum.public_file_translation.value, TranslationTaskNameEnum.private_file_translation.value]
                }
            }
        )

        tasks_id = list(map(lambda task: task.id.value, tasks))

        print(f'Total tasks: {len(tasks)}')
        print(f'Total test is total tasks: {len(tasks)}')

        total_test = 0
        success_test = 0

        for task_id in tasks_id:
            try:
                # Get translation request result and transaltion history
                tasks_result_and_trans_history_req = [
                    translation_request_result_repository.find_many(
                        params=dict(
                            task_id={
                                '$in': list(map(lambda t: UUID(t), [task_id]))
                            },
                            step=TranslationTaskStepEnum.translating_language.value
                        )
                    ),
                    translation_history_repository.find_many(
                        params=dict(
                            task_id={
                                '$in': list(map(lambda t: UUID(t), [task_id]))
                            }
                        )
                    )
                ]

                tasks_result, translations_history = await asyncio.gather(*tasks_result_and_trans_history_req)

                # Modify tasks result and translation history
                for trans_his in translations_history:
                    trans_his.props.status = TranslationHistoryStatus.translating.value

                filepath = ''
                for tasks_res in tasks_result:
                    data = await tasks_res.read_data_from_file()
                    filepath = data['original_file_full_path']
                    data['status'] = 'translating'
                    await tasks_res.save_request_result_to_file(json.dumps(data))

                # Select chosen tasks only
                chosen_tasks = []

                for task in tasks:
                    if task.id.value == task_id:
                        chosen_tasks.append(task)

                total_test += 1

                valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
                    tasks=chosen_tasks,
                    tasks_result=tasks_result,
                    translations_history=translations_history
                )

                success_test += 1
                print(
                    f'Test run successfully! Check out testcase here: {filepath}')

            except:
                print('Test failed!')

        print(f'Total test passed: {success_test}')
        print(f'Total test failed: {total_test - success_test}')
        print(f'Total test passed percent: {success_test / total_test * 100}%')
        print('=============================================================')

    except:
        traceback.print_exc()
        return


async def test_mark_invalid_tasks():
    print('=====================test_mark_invalid_tasks=====================')
    seed = 31415
    random.seed(seed)
    print(f'Random seed is {seed}')

    try:
        tasks: List[TranslationRequestEntity]
        tasks_result: List[TranslationRequestResultEntity]
        translations_history: List[TranslationHistoryEntity]

        # Get task from database
        tasks = await translation_request_repository.find_many(
            params={
                'task_name': {
                    '$in': [TranslationTaskNameEnum.public_file_translation.value, TranslationTaskNameEnum.private_file_translation.value]
                }
            }
        )

        tasks_id = list(map(lambda task: task.id.value, tasks))

        print(f'Total tasks: {len(tasks)}')
        print(f'Total test is total tasks: {len(tasks)}')

        total_test = 0
        success_test = 0

        for task_id in tasks_id:
            try:
                # Get translation request result and transaltion history
                tasks_result_and_trans_history_req = [
                    translation_request_result_repository.find_many(
                        params=dict(
                            task_id={
                                '$in': list(map(lambda t: UUID(t), [task_id]))
                            },
                            step=TranslationTaskStepEnum.translating_language.value
                        )
                    ),
                    translation_history_repository.find_many(
                        params=dict(
                            task_id={
                                '$in': list(map(lambda t: UUID(t), [task_id]))
                            }
                        )
                    )
                ]

                tasks_result, translations_history = await asyncio.gather(*tasks_result_and_trans_history_req)

                # Modify tasks result and translation history
                for trans_his in translations_history:
                    trans_his.props.status = TranslationHistoryStatus.translating.value

                filepath = ''
                for tasks_res in tasks_result:
                    data = await tasks_res.read_data_from_file()
                    filepath = data['original_file_full_path']
                    data['status'] = 'translating'
                    await tasks_res.save_request_result_to_file(json.dumps(data))

                # Select chosen tasks only
                chosen_tasks = []

                for task in tasks:
                    if task.id.value == task_id:
                        chosen_tasks.append(task)

                valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
                    tasks=chosen_tasks,
                    tasks_result=tasks_result,
                    translations_history=translations_history
                )

                total_test += 1

                await mark_invalid_tasks(invalid_tasks_mapper)

                success_test += 1
                print(
                    f'Test run successfully! Check out testcase here: {filepath}')

            except:
                print('Test failed!')

        print(f'Total test passed: {success_test}')
        print(f'Total test failed: {total_test - success_test}')
        print(f'Total test passed percent: {success_test / total_test * 100}%')
        print('=============================================================')

    except:
        traceback.print_exc()
        return


async def test_execute_in_batch():
    print('=====================test_execute_in_batch=====================')
    seed = 31415
    random.seed(seed)
    print(f'Random seed is {seed}')

    try:
        tasks: List[TranslationRequestEntity]
        tasks_result: List[TranslationRequestResultEntity]
        translations_history: List[TranslationHistoryEntity]

        # Get task from database
        tasks = await translation_request_repository.find_many(
            params={
                'task_name': {
                    '$in': [TranslationTaskNameEnum.public_file_translation.value, TranslationTaskNameEnum.private_file_translation.value]
                }
            }
        )

        tasks_id = list(map(lambda task: task.id.value, tasks))

        print(f'Total tasks: {len(tasks)}')
        print(f'Total test is total tasks: {len(tasks)}')

        total_test = 0
        success_test = 0

        for task_id in tasks_id:
            try:
                # Get translation request result and transaltion history
                tasks_result_and_trans_history_req = [
                    translation_request_result_repository.find_many(
                        params=dict(
                            task_id={
                                '$in': list(map(lambda t: UUID(t), [task_id]))
                            },
                            step=TranslationTaskStepEnum.translating_language.value
                        )
                    ),
                    translation_history_repository.find_many(
                        params=dict(
                            task_id={
                                '$in': list(map(lambda t: UUID(t), [task_id]))
                            }
                        )
                    )
                ]

                tasks_result, translations_history = await asyncio.gather(*tasks_result_and_trans_history_req)

                # Modify tasks result and translation history
                for trans_his in translations_history:
                    trans_his.props.status = TranslationHistoryStatus.translating.value

                filepath = ''
                for tasks_res in tasks_result:
                    data = await tasks_res.read_data_from_file()
                    filepath = data['original_file_full_path']
                    data['status'] = 'translating'
                    await tasks_res.save_request_result_to_file(json.dumps(data))

                # Select chosen tasks only
                chosen_tasks = []

                for task in tasks:
                    if task.id.value == task_id:
                        chosen_tasks.append(task)

                valid_tasks_mapper, invalid_tasks_mapper = await read_task_result(
                    tasks=chosen_tasks,
                    tasks_result=tasks_result,
                    translations_history=translations_history
                )

                await mark_invalid_tasks(invalid_tasks_mapper)

                valid_tasks_id = list(
                    map(lambda t: t, list(valid_tasks_mapper)))
                chunked_tasks_id = list(chunk_arr(valid_tasks_id, 1))

                total_test += 1

                for chunk in chunked_tasks_id:
                    await execute_in_batch(valid_tasks_mapper, chunk, 1)

                success_test += 1
                print(
                    f'Test run successfully! Check out testcase here: {filepath}')

            except:
                print('Test failed!')

        print(f'Total test passed: {success_test}')
        print(f'Total test failed: {total_test - success_test}')
        print(f'Total test passed percent: {success_test / total_test * 100}%')
        print('=============================================================')

    except:
        traceback.print_exc()
        return


async def test_main():
    print('=====================test_main===============================')
    try:
        await main()
        print('Test main successfully!')
    except:
        traceback.print_exc()
        print('Test main failed!')
        return


async def test_all():
    print('Begin testing module translate_file_created_by_public_request.translate_content.txt')
    await test_read_task_result()
    await test_mark_invalid_tasks()
    await test_execute_in_batch()
    await test_main()
