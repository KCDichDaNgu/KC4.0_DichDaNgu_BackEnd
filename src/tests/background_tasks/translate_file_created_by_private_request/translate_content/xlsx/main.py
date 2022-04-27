import json
import traceback
from infrastructure.adapters.logger.main import Logger
from modules.background_tasks.translate_file_created_by_private_request.translate_content.xlsx.main import mark_invalid_tasks, read_task_result, execute_in_batch, main
from modules.background_tasks.translate_file_created_by_private_request.translate_content.xlsx.main import read_task_result
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.translation_history import TranslationHistoryStatus
from core.utils.common import chunk_arr
from docx import Document
from typing import List
from uuid import UUID
from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.task import (
    TranslationTaskNameEnum, 
    TranslationTaskStepEnum
)

from infrastructure.adapters.content_translator.main import ContentTranslator 

from modules.translation_request.database.translation_request.repository import TranslationRequestRepository, TranslationRequestEntity
from modules.translation_request.database.translation_request_result.repository import TranslationRequestResultRepository, TranslationRequestResultEntity
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository, TranslationHistoryEntity, TranslationHistoryRepositoryPort
from modules.system_setting.database.repository import SystemSettingRepository

import asyncio

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

LIMIT_NUM_CHAR_TRANSLATE_REQUEST = 1000000000

translation_request_repository = TranslationRequestRepository()
translation_request_result_repository = TranslationRequestResultRepository()
transation_history_repository = TranslationHistoryRepository()
system_setting_repository = SystemSettingRepository()

contentTranslator = ContentTranslator()

logger = Logger('Task: translate_file_created_by_private_request.translate_content.xlsx')

async def test_mark_invalid_tasks():
    print('=====================test_mark_invalid_tasks=====================')

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
                    TranslationHistoryRepositoryPort.find_many(
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
                    transation_history_repository.find_many(
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
    await test_mark_invalid_tasks()
    await test_execute_in_batch()
    await test_main()
