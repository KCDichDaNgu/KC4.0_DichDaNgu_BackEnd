from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.language_detection_request.database.language_detection_request_result.orm_entity import LanguageDetectionRequestResultOrmEntity
from modules.language_detection_request.domain.entities.language_detection_request_result import LanguageDetectionRequestResultEntity, LanguageDetectionRequestResultProps

from modules.task.database.task_result.orm_mapper import TaskResultOrmMapper
from core.value_objects import ID

from typing import get_args

class LanguageDetectionRequestResultOrmMapper(
    TaskResultOrmMapper, 
    OrmMapperBase[
        LanguageDetectionRequestResultEntity, 
        LanguageDetectionRequestResultOrmEntity
    ]
):
    
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[1])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[1])[1]

    def to_orm_props(self, entity: LanguageDetectionRequestResultEntity):
        
        props = entity.get_props_copy()
        
        orm_props = {
            'task_id': props.task_id.value,
            'step': props.step,
            'file_path': props.file_path
        }
        
        return orm_props

    def to_domain_props(self, orm_entity: LanguageDetectionRequestResultOrmEntity):

        props = {
            'task_id': ID(str(orm_entity.task_id)),
            'step': orm_entity.step,
            'file_path': orm_entity.file_path
        }

        return props
