from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.translation_request.database.translation_request_result.orm_entity import TranslationRequestResultOrmEntity
from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultEntity, TranslationRequestResultProps

from modules.task.database.task_result.orm_mapper import TaskResultOrmMapper
from core.value_objects import ID

from typing import get_args

class TranslationRequestResultOrmMapper(
    TaskResultOrmMapper, 
    OrmMapperBase[
        TranslationRequestResultEntity, 
        TranslationRequestResultOrmEntity
    ]
):
    
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[1])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[1])[1]

    def to_orm_props(self, entity: TranslationRequestResultEntity):
        
        props = entity.get_props_copy()
        
        orm_props = {
            'task_id': props.task_id.value,
            'step': props.step,
            'file_path': props.file_path
        }
        
        return orm_props

    def to_domain_props(self, orm_entity: TranslationRequestResultOrmEntity):

        props = {
            'task_id': ID(str(orm_entity.task_id)),
            'step': orm_entity.step,
            'file_path': orm_entity.file_path
        }

        return props
