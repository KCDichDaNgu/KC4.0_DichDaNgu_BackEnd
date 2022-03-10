from datetime import datetime, timedelta

from uuid import UUID
from modules.language_detection_request.database.language_detection_history.repository import LanguageDetectionHistoryRepository
from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository

from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.task import (
    StepStatusEnum,
    get_task_result_file_path
)
from modules.task.database.task_result.repository import TasktResultRepository
from modules.task.database.task.repository import TaskRepository
from modules.system_setting.database.repository import SystemSettingRepository

from core.utils.file import delete_files, delete_folders
import asyncio
from infrastructure.adapters.logger import Logger
from infrastructure.configs.translation_task import FILE_TRANSLATION_TASKS, PLAIN_TEXT_TRANSLATION_TASKS, get_file_translation_file_path
from infrastructure.configs.language_detection_task import get_file_language_detection_file_path

config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()

translation_history_repository = TranslationHistoryRepository()
language_detection_history_repository = LanguageDetectionHistoryRepository()
task_repository = TaskRepository()
task_result_repository = TasktResultRepository()
system_setting_repository = SystemSettingRepository()

logger = Logger('Task: delete_invalid_task')

async def main():

    logger.debug(
        msg=f'New task delete_invalid_task run in {datetime.now()}'
    )

    print(f'New task delete_invalid_task run in {datetime.now()}')

    try:
        
        system_setting = await system_setting_repository.find_one({})
        
        task_expired_duration = system_setting.props.task_expired_duration

        invalid_tasks = await task_repository.find_many(
           params={
                "$and": [
                    {
                        "$and": [
                            {
                                "step_status": {
                                    "$in": [
                                        StepStatusEnum.cancelled.value,
                                        StepStatusEnum.closed.value,
                                    ]
                                }
                            },
                            {"created_at": {"$lt": datetime.now() - timedelta(seconds=task_expired_duration)}},
                        ],
                    },
                    {
                       "task_name": {
                           "$in": [PLAIN_TEXT_TRANSLATION_TASKS, FILE_TRANSLATION_TASKS]
                       } 
                    }
                ]
            }
        )

        invalid_tasks_ids = list(map(lambda task: task.id.value, invalid_tasks)) if not invalid_tasks is None else []

        invalid_tasks_results = []

        invalid_tasks_results = await task_result_repository.find_many(
            params={
                "task_id": {
                    "$in": [UUID(task_id) for task_id in invalid_tasks_ids]
                }
            }
        )

        invalid_tasks_file_paths = list(map(lambda task: task.props.file_path, invalid_tasks_results))
        task_results_file_paths, file_translation_folders, language_detection_folders = get_to_be_deleted_file_path(invalid_tasks_file_paths)

        if len(invalid_tasks_ids) == 0:
            logger.debug(
                msg=f'An task delete_invalid_task end in {datetime.now()}\n')

            print(f'An task delete_invalid_task end in {datetime.now()}\n')
            return

        async with db_instance.session() as session:

            async with session.start_transaction():

                clean_request = []

                clean_request.append(
                    language_detection_history_repository.delete_many_by_condition(
                        conditions=[{"task_id": invalid_tasks_ids}]
                    )
                )

                clean_request.append(
                    translation_history_repository.delete_many_by_condition(
                        conditions=[{"task_id": invalid_tasks_ids}]
                    )
                )

                clean_request.append(
                    task_result_repository.delete_many_by_condition(
                        conditions=[{"task_id": invalid_tasks_ids}]
                    )
                )

                clean_request.append(
                    task_repository.delete_many_by_condition(
                        conditions=[{"_id": invalid_tasks_ids}]
                    )
                )

                await delete_files(task_results_file_paths)

                await delete_folders(file_translation_folders + language_detection_folders)

                await asyncio.gather(*clean_request)

    except Exception as e:
        logger.error(e)

        print(e)

    logger.debug(
        msg=f'An task delete_invalid_task end in {datetime.now()}\n'
    )

def get_task_id_from_task_result_file_path(file_path):

    return (file_path.split('.')[0]).split('__')[-1]

def get_to_be_deleted_file_path(invalid_file_paths):

    task_results_file_paths = list(
        map(
            lambda f_path: get_task_result_file_path(f_path),
            invalid_file_paths,
        )
    )
    task_ids = list(
        map(
            lambda f_path: get_task_id_from_task_result_file_path(f_path),
            invalid_file_paths,
        )
    )

    file_translation_folders = list(
        map(
            lambda f_path: get_file_translation_file_path(f_path, ""),
            task_ids,
        )
    )
    language_detection_folders = list(
        map(
            lambda f_path: get_file_language_detection_file_path(f_path, ""),
            task_ids,
        )
    )

    return task_results_file_paths, file_translation_folders, language_detection_folders
