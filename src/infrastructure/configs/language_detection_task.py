from infrastructure.configs.language import LanguageEnum
from typing import Optional, Union
from pydantic.fields import Field
from pydantic.main import BaseModel
from core.types import ExtendedEnum


FILE_LANGUAGE_DETECTION_FOLDER_PATH = 'file_language_detection'
FILE_LANGUAGE_DETECTION_SOURCE_FILE_NAME = 'source_file'


def get_file_language_detection_file_path(task_id, file_name: str):

    return f'{FILE_LANGUAGE_DETECTION_FOLDER_PATH}/{task_id}/{file_name}'

def get_file_language_detection_source_file_name():

    return FILE_LANGUAGE_DETECTION_SOURCE_FILE_NAME


class LanguageDetectionTaskNameEnum(str, ExtendedEnum):

    private_file_language_detection = 'private_file_language_detection'
    private_plain_text_language_detection = 'private_plain_text_language_detection'

    public_file_language_detection = 'public_file_language_detection'
    public_plain_text_language_detection = 'public_plain_text_language_detection'

LANGUAGE_DETECTION_PUBLIC_TASKS = [
    LanguageDetectionTaskNameEnum.public_file_language_detection.value,
    LanguageDetectionTaskNameEnum.public_plain_text_language_detection.value
]

LANGUAGE_DETECTION_PRIVATE_TASKS = [
    LanguageDetectionTaskNameEnum.private_file_language_detection.value,
    LanguageDetectionTaskNameEnum.private_plain_text_language_detection.value
]

FILE_LANGUAGE_DETECTION_TASKS = [
    LanguageDetectionTaskNameEnum.private_file_language_detection.value,
    LanguageDetectionTaskNameEnum.public_file_language_detection.value
]

class LanguageDetectionTaskStepEnum(str, ExtendedEnum):

    detecting_language = 'detecting_language'

RESULT_FILE_STATUS = {
    'language_not_yet_detected': 'language_not_yet_detected',
    'closed': 'closed',
    'language_detected': 'language_detected'
}

class LanguageDetectionTask_LangUnknownResultFileSchemaV1(BaseModel):

    source_text: str 
    source_lang: Union[LanguageEnum, None] = Field(None, allow_mutation=False) 

    task_name: LanguageDetectionTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['language_not_yet_detected'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class LanguageDetectionTask_LanguageDetectionClosedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum

    task_name: LanguageDetectionTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['closed'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True

class LanguageDetectionTask_LanguageDetectionCompletedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum

    task_name: LanguageDetectionTaskNameEnum 
    
    status: str = Field(RESULT_FILE_STATUS['language_detected'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True



class FileLanguageDetectionTask_LangUnknownResultFileSchemaV1(BaseModel):

    source_file_full_path: str
    source_lang: Union[LanguageEnum, None] = Field(None, allow_mutation=False) 
    file_type: str
    task_name: LanguageDetectionTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['language_not_yet_detected'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class FileLanguageDetectionTask_LanguageDetectionClosedResultFileSchemaV1(BaseModel):

    source_file_full_path: str
    source_lang: LanguageEnum
    file_type: str
    task_name: LanguageDetectionTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['closed'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True

class FileLanguageDetectionTask_LanguageDetectionCompletedResultFileSchemaV1(BaseModel):

    source_file_full_path: str
    source_lang: LanguageEnum
    file_type: str
    task_name: LanguageDetectionTaskNameEnum 
    
    status: str = Field(RESULT_FILE_STATUS['language_detected'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True