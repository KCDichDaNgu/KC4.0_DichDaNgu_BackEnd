from core.value_objects.id import ID
from typing import Any, get_args
from infrastructure.database.base_classes.mongodb.orm_mapper_base import OrmMapperBase

from modules.user.database.user.orm_entity import UserOrmEntity
from modules.user.domain.entities.user import UserEntity, UserProps

class UserOrmMapper(OrmMapperBase[UserEntity, UserOrmEntity]):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def orm_entity_klass(self):
        return get_args(self.__orig_bases__[0])[1]

    def to_orm_props(self, entity: UserEntity) -> Any:
        
        props = entity.get_props_copy()
        
        orm_props = {
            'username': props.username,
            'first_name': props.first_name,
            'last_name': props.last_name,
            'email': props.email,
            'password': props.password,
            'avatar': props.avatar,
            'role': props.role,
            'status': props.status,
        }

        return orm_props

    def to_domain_props(self, orm_entity: UserOrmEntity) -> UserProps:
        
        props = {
            'username': orm_entity.username,
            'first_name': orm_entity.first_name,
            'last_name': orm_entity.last_name,
            'email': orm_entity.email,
            'password': orm_entity.password,
            'avatar': orm_entity.avatar,
            'role': orm_entity.role,
            'status': orm_entity.status,
        }

        return props
        