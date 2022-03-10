from core.value_objects import ID
from typing import Any, get_args
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.user.database.token.orm_entity import TokenOrmEntity
from modules.user.domain.entities.token import TokenEntity, TokenProps

class TokenOrmMapper(OrmMapperBase[TokenEntity, TokenOrmEntity]):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[0])[1]

    def to_orm_props(self, entity: TokenEntity) -> Any:
        
        props = entity.get_props_copy()

        orm_props = {
            'user_id': props.user_id.value,
            'token_type': props.token_type,
            'access_token': props.access_token.value,
            'refresh_token': props.refresh_token.value,
            'scope': props.scope,
            'access_expires_in': props.access_expires_in,
            'refresh_expires_in': props.refresh_expires_in,
            'platform': props.platform,
            'revoked': props.revoked
        }

        return orm_props

    def to_domain_props(self, orm_entity: TokenOrmEntity) -> TokenProps:
        
        props = {
            'user_id': ID(str(orm_entity.user_id)),
            'token_type': orm_entity.token_type,
            'access_token': ID(str(orm_entity.access_token)),
            'refresh_token': ID(str(orm_entity.refresh_token)),
            'scope': orm_entity.scope,
            'access_expires_in': orm_entity.access_expires_in,
            'refresh_expires_in': orm_entity.refresh_expires_in,
            'platform': orm_entity.platform,
            'revoked': orm_entity.revoked
        }

        return props
