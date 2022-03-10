from core.value_objects import ID, DateVO
from typing import Any
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.language_detection_request.database.language_detection_history.orm_entity import LanguageDetectionHistoryOrmEntity
from modules.language_detection_request.domain.entities.language_detection_history import LanguageDetectionHistoryEntity, LanguageDetectionHistoryProps

from typing import get_args

class LanguageDetectionHistoryOrmMapper(OrmMapperBase[LanguageDetectionHistoryEntity, LanguageDetectionHistoryOrmEntity]):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[0])[1]

    def to_orm_props(self, entity: LanguageDetectionHistoryEntity):
        
        props = entity.get_props_copy()
        
        orm_props = {
            'creator_id': props.creator_id.value,
            'task_id': props.task_id.value,
            'language_detection_type': props.language_detection_type,
            'status': props.status,
            'file_path': props.file_path
        }
        
        return orm_props

    def to_domain_props(self, orm_entity: LanguageDetectionHistoryOrmEntity):

        props = {
            'creator_id': ID(str(orm_entity.creator_id)),
            'task_id': ID(str(orm_entity.task_id)),
            'language_detection_type': orm_entity.language_detection_type,
            'status': orm_entity.status,
            'file_path': orm_entity.file_path,
        }

        return props
