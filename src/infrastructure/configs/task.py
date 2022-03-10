from core.types import ExtendedEnum

from infrastructure.configs.translation_task import *
from infrastructure.configs.language_detection_task import *

TASK_EXPIRATION_TIME = 60 * 60
TASK_RESULT_FOLDER = 'task_result'
TASK_RESULT_FILE_PATTERN = '{}__{}.{}'
TASK_RESULT_FILE_EXTENSION = 'json'


def get_task_result_file_path(file_name):

    return f'{TASK_RESULT_FOLDER}/{file_name}'

def get_task_result_file_name(created_at, task_id, file_extension):

    return TASK_RESULT_FILE_PATTERN.format(
        created_at, 
        task_id,
        file_extension
    )

class TaskTypeEnum(str, ExtendedEnum):

    unclassified = 'unclassified'
    translation_task = 'translation_task'
    language_detection = 'language_detection'

class CreatorTypeEnum(str, ExtendedEnum):

    end_user = 'end_user'

class StepStatusEnum(str, ExtendedEnum):

    not_yet_processed = 'not_yet_processed' # Chưa chạy
    in_progress = 'in_progress' # Trong trường hợp task bị kéo dài, k rõ bao h xong 
    
    completed = 'completed' # Hoàn thành

    closed = 'closed' # Bị đóng do nguyên nhân end user
    cancelled = 'cancelled' # Bị đóng do lỗi bên phía server
