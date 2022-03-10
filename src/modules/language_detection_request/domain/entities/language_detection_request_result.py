
import os
from time import time
from pydantic import Field
from typing import Optional

from sanic.request import File
from core.base_classes.entity import Entity
from core.value_objects import ID
from modules.task.domain.entities.task_result import TaskResultEntity, TaskResultProps

from typing import get_args
from core.utils.file import extract_file_extension, get_full_path
from infrastructure.configs.main import StatusCodeEnum

from interface_adapters.dtos.base_response import BaseResponse
from infrastructure.configs.message import MESSAGES
from infrastructure.configs.language_detection_task import FILE_LANGUAGE_DETECTION_FOLDER_PATH, get_file_language_detection_file_path, get_file_language_detection_source_file_name

class LanguageDetectionRequestResultProps(TaskResultProps):
    
    task_id: ID = Field(...)
    step: str = Field(...)
    file_path: Optional[str]

class LanguageDetectionRequestResultEntity(
    TaskResultEntity, 
    Entity[LanguageDetectionRequestResultProps]
):

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[1])[0]

    def __create_file_language_translation_task_folder(self):
            real_file_language_translation_task_folder = get_full_path(f'{FILE_LANGUAGE_DETECTION_FOLDER_PATH}/{self.props.task_id.value}')

            if not os.path.isdir(real_file_language_translation_task_folder):

                os.makedirs(real_file_language_translation_task_folder)

            return real_file_language_translation_task_folder

    async def create_required_files_for_file_language_detection_task(self, source_file: File):

        self.__create_file_language_translation_task_folder()

        source_file_ext = extract_file_extension(source_file.name)

        source_file_name = f'{get_file_language_detection_source_file_name()}.{source_file_ext}'
        source_file_path = get_file_language_detection_file_path(self.props.task_id.value, source_file_name)
        source_file_full_path = get_full_path(source_file_path)
        
        try:
            with open(source_file_full_path, 'wb+') as outp:

                outp.write(source_file.body)

                outp.close()
        
        except Exception as e:
            return BaseResponse(
                code=StatusCodeEnum.failed.value,
                data=dict(
                    source_file_full_path=None
                ),
                message=MESSAGES['failed']
            )
        
        return BaseResponse(
                code=StatusCodeEnum.failed.value,
                data=dict(
                    source_file_full_path=source_file_full_path
                ),
                message=MESSAGES['failed']
            )
