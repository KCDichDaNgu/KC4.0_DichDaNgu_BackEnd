from core.value_objects import ID, DateVO
from typing import Any
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.translation_request.database.translation_history.orm_entity import TranslationHistoryOrmEntity
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity, TranslationHistoryProps

from typing import get_args

class TranslationHistoryOrmMapper(OrmMapperBase[TranslationHistoryEntity, TranslationHistoryOrmEntity]):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[0])[1]

    def to_orm_props(self, entity: TranslationHistoryEntity):
        
        props = entity.get_props_copy()
        
        orm_props = {
            'creator_id': props.creator_id.value,
            'task_id': props.task_id.value,
            'translation_type': props.translation_type,
            'status': props.status,
            'file_path': props.file_path,
            'rating': props.rating,
            'user_edited_translation': props.user_edited_translation,
            'user_updated_at': props.user_updated_at.value if props.user_updated_at else None,
            'source_lang': props.source_lang,
            'target_lang': props.target_lang
        }
        
        return orm_props

    def to_domain_props(self, orm_entity: TranslationHistoryOrmEntity):

        props = {
            'creator_id': ID(str(orm_entity.creator_id)),
            'task_id': ID(str(orm_entity.task_id)),
            'translation_type': orm_entity.translation_type,
            'status': orm_entity.status,
            'file_path': orm_entity.file_path,
            'rating': orm_entity.rating,
            'user_edited_translation': orm_entity.user_edited_translation,
            'user_updated_at': DateVO(orm_entity.user_updated_at),
            'source_lang': orm_entity.source_lang,
            'target_lang': orm_entity.target_lang
        }

        return props
