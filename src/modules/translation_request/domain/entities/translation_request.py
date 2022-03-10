from sanic.request import File
from pydantic.class_validators import root_validator
from typing import Optional, Union, IO
import io
import openpyxl
from pydantic import Field
from infrastructure.configs.translation_task import FILE_TRANSLATION_TASKS, PLAIN_TEXT_TRANSLATION_TASKS, AllowedFileTranslationExtensionEnum

from core.base_classes.aggregate_root import AggregateRoot

from modules.task.domain.entities.task import TaskEntity, TaskProps

from typing import get_args
from core.utils.file import get_doc_file_meta, get_presentation_file_meta, get_worksheet_file_meta, get_txt_file_meta

from core.utils.text import count_chars

from infrastructure.configs.task import (
    TranslationTaskStepEnum, 
    TranslationTaskNameEnum,
    TRANSLATION_PRIVATE_TASKS,
)

class TranslationRequestProps(TaskProps):

    current_step: TranslationTaskStepEnum = Field(...)
    task_name: TranslationTaskNameEnum = Field(...)
    
    num_chars: int = 0
    
    receiver_email: Optional[str]
    total_email_sent: Optional[int] 

    @root_validator(pre=True)
    def validate(cls, values):
        
        if values['task_name'] in TRANSLATION_PRIVATE_TASKS and not values['creator_id'].value:
            raise ValueError('Creator cannot be None')

        return values

class TranslationRequestEntity(TaskEntity, AggregateRoot[TranslationRequestProps]):    

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[1])[0]
    
    async def update_num_chars(self, doc):
        
        if self.props.task_name in PLAIN_TEXT_TRANSLATION_TASKS:
            
            self.props.num_chars = count_chars(doc)
            
            return
        
        if self.props.task_name in FILE_TRANSLATION_TASKS:
            
            if self.props.file_type == AllowedFileTranslationExtensionEnum.docx.value:
            
                binary_doc, total_doc_paragraphs, character_count = get_doc_file_meta(doc)
                
                self.props.num_chars = character_count
                
            if self.props.file_type == AllowedFileTranslationExtensionEnum.pptx.value:
                
                binary_presentation, total_presentation_paragraphs, total_slides, character_count = get_presentation_file_meta(doc)
                
                self.props.num_chars = character_count
                
            if self.props.file_type == AllowedFileTranslationExtensionEnum.xlsx.value:
                
                binary_worksheet, total_sheets, total_cells, character_count = get_worksheet_file_meta(doc)
                
                self.props.num_chars = character_count
                
            if self.props.file_type == AllowedFileTranslationExtensionEnum.txt.value:
                    
                self.props.num_chars = get_txt_file_meta(doc)
