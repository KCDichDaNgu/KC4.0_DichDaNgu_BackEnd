from core.value_objects import ID
from typing import Any, get_args
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.user.database.user_statistic.orm_entity import UserStatisticOrmEntity
from modules.user.domain.entities.user_statistic import UserStatisticEntity, UserStatisticProps

class UserStatisticOrmMapper(OrmMapperBase[UserStatisticEntity, UserStatisticOrmEntity]):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[0])[1]

    def to_orm_props(self, entity: UserStatisticEntity) -> Any:
        
        props = entity.get_props_copy()

        orm_props = {
            'user_id': props.user_id.value,
            'total_translated_text': props.total_translated_text,
            'text_translation_quota': props.text_translation_quota,
        }

        return orm_props

    def to_domain_props(self, orm_entity: UserStatisticOrmEntity) -> UserStatisticProps:
        
        props = {
            'user_id': ID(str(orm_entity.user_id)),
            'total_translated_text': orm_entity.total_translated_text,
            'text_translation_quota': orm_entity.text_translation_quota,
        }

        return props
