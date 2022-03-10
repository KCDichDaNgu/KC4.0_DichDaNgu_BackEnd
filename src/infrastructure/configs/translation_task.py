from infrastructure.configs.language import LanguageEnum
from typing import Dict, Optional, Union
from pydantic.fields import Field
from pydantic.main import BaseModel
from core.types import ExtendedEnum

from core.utils.file import extract_file_extension

FILE_TRANSLATION_FOLDER_PATH = 'file_translation'
FILE_TRANSLATION_SOURCE_FILE_NAME = 'source_file'
FILE_TRANSLATION_BINARY_PROGRESS_FILE_NAME = 'binary_progress_file'
FILE_TRANSLATION_TARGET_FILE_NAME = 'target_file'

RESULT_FILE_STATUS = {
    'language_not_yet_detected': 'language_not_yet_detected',
    'not_yet_translated': 'not_yet_translated',
    'closed': 'closed',
    'translated': 'translated',
    'translating': 'translating'
}

class AllowedFileTranslationExtensionEnum(str, ExtendedEnum):

    txt = 'txt'
    docx = 'docx'
    pptx = 'pptx'
    xlsx = 'xlsx'

def is_allowed_file_extension(file_name):

    file_ext = extract_file_extension(file_name)

    return file_ext in AllowedFileTranslationExtensionEnum.enum_values()

def get_file_translation_file_path(task_id, file_name: str):

    return f'{FILE_TRANSLATION_FOLDER_PATH}/{task_id}/{file_name}'

def get_file_translation_source_file_name():

    return FILE_TRANSLATION_SOURCE_FILE_NAME

def get_file_translation_target_file_name():

    return FILE_TRANSLATION_TARGET_FILE_NAME

def get_file_translation_binary_progress_file_name():

    return FILE_TRANSLATION_BINARY_PROGRESS_FILE_NAME

class TranslationTaskNameEnum(str, ExtendedEnum):

    private_file_translation = 'private_file_translation'
    private_plain_text_translation = 'private_plain_text_translation'

    public_file_translation = 'public_file_translation'
    public_plain_text_translation = 'public_plain_text_translation'

TRANSLATION_PUBLIC_TASKS = [
    TranslationTaskNameEnum.public_file_translation.value,
    TranslationTaskNameEnum.public_plain_text_translation.value
]

TRANSLATION_PRIVATE_TASKS = [
    TranslationTaskNameEnum.private_file_translation.value,
    TranslationTaskNameEnum.private_plain_text_translation.value
]

PLAIN_TEXT_TRANSLATION_TASKS = [
    TranslationTaskNameEnum.public_plain_text_translation.value,
    TranslationTaskNameEnum.private_plain_text_translation.value
]

FILE_TRANSLATION_TASKS = [
    TranslationTaskNameEnum.private_file_translation.value,
    TranslationTaskNameEnum.public_file_translation.value
]

class TranslationTaskStepEnum(str, ExtendedEnum):
    
    detecting_language = 'detecting_language'
    translating_language = 'translating_language'

class DocumentStatistic(BaseModel):
    total_paragraphs: Optional[int]
    total_slides: Optional[int]
    total_sheets: Optional[int]

class DocumentCurrentProgress(BaseModel):
    processed_paragraph_index: Optional[int]
    processed_slide_index: Optional[int]
    processed_sheet_index: Optional[int]
    last_row: Optional[int]
    last_col: Optional[int]

class TranslationTask_LangUnknownResultFileSchemaV1(BaseModel):

    source_text: str 
    source_lang: Union[LanguageEnum, None] = Field(None, allow_mutation=False)

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['language_not_yet_detected'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class TranslationTask_NotYetTranslatedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum 

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['not_yet_translated'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class TranslationTask_NotYetTranslatedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum 

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['not_yet_translated'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class TranslationTask_TranslationClosedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum

    target_text: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['closed'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True

class TranslationTask_TranslationCompletedResultFileSchemaV1(BaseModel):

    source_text: str
    source_lang: LanguageEnum

    target_text: str
    target_lang: LanguageEnum

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['translated'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True

class FileTranslationTask_LangUnknownResultFileSchemaV1(BaseModel):

    original_file_full_path: str
    file_type:str
    binary_progress_file_full_path: Optional[str]
    statistic: DocumentStatistic
    current_progress: DocumentCurrentProgress
    
    source_lang: Union[LanguageEnum, None] = Field(None, allow_mutation=False)

    target_file_full_path: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['language_not_yet_detected'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True

class FileTranslationTask_NotYetTranslatedResultFileSchemaV1(BaseModel):

    original_file_full_path: str
    file_type:str
    binary_progress_file_full_path: Optional[str]
    statistic: DocumentStatistic
    current_progress: DocumentCurrentProgress

    source_lang: LanguageEnum 

    target_file_full_path: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum 

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['not_yet_translated'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False) 

    class Config:
        use_enum_values = True
        validate_assignment = True


class FileTranslationTask_TranslationClosedResultFileSchemaV1(BaseModel):

    original_file_full_path: str
    file_type:str
    binary_progress_file_full_path: Optional[str]
    statistic: DocumentStatistic
    current_progress: DocumentCurrentProgress

    source_lang: LanguageEnum

    target_file_full_path: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['closed'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True
class FileTranslationTask_TranslatingResultFileSchemaV1(BaseModel):

    original_file_full_path: str
    file_type:str
    binary_progress_file_full_path: Optional[str]
    statistic: DocumentStatistic
    current_progress: DocumentCurrentProgress

    source_lang: LanguageEnum

    target_file_full_path: Union[str, None] = Field(None, allow_mutation=False)
    target_lang: LanguageEnum

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['translating'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True

class FileTranslationTask_TranslationCompletedResultFileSchemaV1(BaseModel):

    original_file_full_path: str
    file_type:str
    binary_progress_file_full_path: Optional[str]
    statistic: DocumentStatistic
    current_progress: DocumentCurrentProgress

    source_lang: LanguageEnum
    target_file_full_path: str
    target_lang: LanguageEnum

    task_name: TranslationTaskNameEnum

    status: str = Field(RESULT_FILE_STATUS['translated'], allow_mutation=False) 
    message: str = ''

    schema_version: int = Field(1, allow_mutation=False)  

    class Config:
        use_enum_values = True
        validate_assignment = True
