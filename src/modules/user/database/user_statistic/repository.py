from modules.user.database.user_statistic.orm_entity import UserStatisticOrmEntity
from modules.user.database.user_statistic.orm_mapper import UserStatisticOrmMapper
from core.ports.repository import RepositoryPort
from modules.user.domain.entities.user_statistic import UserStatisticEntity, UserStatisticProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase
from typing import get_args

class UserStatisticRepositoryPort(RepositoryPort[UserStatisticEntity, UserStatisticProps]):

    pass

class UserStatisticRepository(OrmRepositoryBase[UserStatisticEntity, UserStatisticProps, UserStatisticOrmEntity, UserStatisticOrmMapper], UserStatisticRepositoryPort):
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def repository(self):
        return get_args(self.__orig_bases__[0])[2]

    @property
    def mapper(self):
        return get_args(self.__orig_bases__[0])[3]
