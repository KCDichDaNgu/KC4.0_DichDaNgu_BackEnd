from datetime import datetime, timedelta
import os

from os.path import getctime
from os import listdir
import aiofiles
import numpy as np

from infrastructure.configs.main import GlobalConfig, get_cnf, get_mongodb_instance
from modules.task.database.task_result.repository import TasktResultRepository
from core.utils.file import delete_files, delete_folders, get_full_path
from infrastructure.adapters.logger import Logger
from infrastructure.configs.task import TASK_EXPIRATION_TIME, TASK_RESULT_FOLDER, get_task_result_file_path
from infrastructure.configs.language_detection_task import get_file_language_detection_file_path
from infrastructure.configs.translation_task import get_file_translation_file_path


config: GlobalConfig = get_cnf()
db_instance = get_mongodb_instance()
task_results_dir = get_full_path(f'{TASK_RESULT_FOLDER}/')

task_result_repository = TasktResultRepository()

logger = Logger('Task: delete_invalid_file')

QUERY_SIZE = 3


async def main():

    logger.debug(
        msg=f'New task delete_invalid_file run in {datetime.now()}'
    )

    print(f'New task delete_invalid_file run in {datetime.now()}')

    try:

        milestone = datetime.now() - timedelta(0, TASK_EXPIRATION_TIME)

        saved_file_paths = [f for f in listdir(task_results_dir) if (get_file_created_time(f) < milestone)]

        while len(saved_file_paths) > 0:

            to_be_check_file_paths = saved_file_paths[:QUERY_SIZE]

            del saved_file_paths[:QUERY_SIZE]

            task_results = await task_result_repository.find_many(
                params={
                    "file_path": {
                        "$in": to_be_check_file_paths
                    }
                }
            )

            task_results_file_paths = list(map(lambda task: task.props.file_path, task_results))

            invalid_file_paths = np.setxor1d(to_be_check_file_paths, task_results_file_paths)

            task_results_file_paths, file_translation_folders, language_detection_folders = get_to_be_deleted_file_path(invalid_file_paths)

            await delete_files(task_results_file_paths)

            await delete_folders(file_translation_folders + language_detection_folders)

        logger.debug(
            msg=f'An task delete_invalid_file end in {datetime.now()}\n')

        print(f'An task delete_invalid_file end in {datetime.now()}\n')

    except Exception as e:
        logger.error(e)

        print(e)

    logger.debug(
        msg=f'An task delete_invalid_file  end in {datetime.now()}\n'
    )


def get_file_created_time(file):

    return datetime.utcfromtimestamp(getctime(get_full_path(get_task_result_file_path(file))))

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