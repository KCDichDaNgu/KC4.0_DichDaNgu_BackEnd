from pydantic.class_validators import root_validator
from typing import Union
from pydantic import Field
from infrastructure.configs.task import (
    LanguageDetectionTaskStepEnum, 
    LanguageDetectionTaskNameEnum,
    LANGUAGE_DETECTION_PRIVATE_TASKS
)

from core.base_classes.aggregate_root import AggregateRoot

from modules.task.domain.entities.task import TaskEntity, TaskProps

from typing import get_args

class LanguageDetectionRequestProps(TaskProps):

    current_step: LanguageDetectionTaskStepEnum = Field(...)
    task_name: LanguageDetectionTaskNameEnum = Field(...)

    @root_validator(pre=True)
    def validate(cls, values):
        
        if values['task_name'] in LANGUAGE_DETECTION_PRIVATE_TASKS and not values['creator_id'].value:
            raise ValueError('Creator cannot be None')

        return values

class LanguageDetectionRequestEntity(TaskEntity, AggregateRoot[LanguageDetectionRequestProps]):

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[1])[0]
