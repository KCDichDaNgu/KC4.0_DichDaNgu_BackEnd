from modules.user.database.user.orm_entity import UserOrmEntity
from modules.user.database.user.orm_mapper import UserOrmMapper
from core.ports.repository import RepositoryPort
from modules.user.domain.entities.user import UserEntity, UserProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase
from typing import get_args

class UserRepositoryPort(RepositoryPort[UserEntity, UserProps]):

    pass

class UserRepository(OrmRepositoryBase[UserEntity, UserProps, UserOrmEntity, UserOrmMapper], UserRepositoryPort):
    
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def repository(self):
        return get_args(self.__orig_bases__[0])[2]

    @property
    def mapper(self):
        return get_args(self.__orig_bases__[0])[3]
