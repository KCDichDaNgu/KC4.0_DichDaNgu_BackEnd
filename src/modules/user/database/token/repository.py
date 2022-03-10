from modules.user.database.token.orm_entity import TokenOrmEntity
from modules.user.database.token.orm_mapper import TokenOrmMapper
from core.ports.repository import RepositoryPort
from modules.user.domain.entities.token import TokenEntity, TokenProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase
from typing import get_args

class TokenRepositoryPort(RepositoryPort[TokenEntity, TokenProps]):

    pass

class TokenRepository(OrmRepositoryBase[TokenEntity, TokenProps, TokenOrmEntity, TokenOrmMapper], TokenRepositoryPort):
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def repository(self):
        return get_args(self.__orig_bases__[0])[2]

    @property
    def mapper(self):
        return get_args(self.__orig_bases__[0])[3]
