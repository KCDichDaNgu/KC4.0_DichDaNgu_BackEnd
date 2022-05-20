from infrastructure.configs.language_detection_task import LanguageDetectionTaskNameEnum
from pydantic.class_validators import root_validator
from typing import Optional, Union, get_args
from pydantic import Field, BaseModel
from infrastructure.configs.task import (
    TranslationTaskNameEnum, 
    CreatorTypeEnum, 
    StepStatusEnum, 
    TranslationTaskStepEnum, 
    LanguageDetectionTaskStepEnum, 
    AllowedFileTranslationExtensionEnum,
    TRANSLATION_PRIVATE_TASKS
)

from core.base_classes.aggregate_root import AggregateRoot
from core.value_objects import DateVO, ID

class TaskProps(BaseModel):

    creator_id: ID
    task_name: Union[TranslationTaskNameEnum, LanguageDetectionTaskNameEnum] = Field(...)
    creator_type: CreatorTypeEnum = Field(...)
    step_status: StepStatusEnum = Field(...)
    current_step: Union[TranslationTaskStepEnum, LanguageDetectionTaskStepEnum] = Field(...)
    file_type: Optional[AllowedFileTranslationExtensionEnum]
    retry: int 
    error_message: Optional[str] = ''
    
    # expired_date: DateVO = DateVO(None)

    class Config:
        use_enum_values = True

    @root_validator(pre=True)
    def validate(cls, values):
        
        if values['task_name'] in TRANSLATION_PRIVATE_TASKS and not values['creator_id'].value:
            raise ValueError('Creator cannot be None')
        
        if 'retry' not in values or not values['retry']: values['retry'] = 0

        return values

class TaskEntity(AggregateRoot[TaskProps]):
    
    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    pass
