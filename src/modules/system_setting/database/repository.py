from typing import get_args
from modules.system_setting.database.orm_mapper import SystemSettingOrmMapper
from modules.system_setting.domain.entities.system_setting import SystemSettingEntity, SystemSettingProps
from modules.system_setting.database.orm_entity import SystemSettingOrmEntity
from core.ports.repository import RepositoryPort
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

class SystemSettingRepositoryPort(RepositoryPort[SystemSettingEntity, SystemSettingOrmEntity]):

    pass

class SystemSettingRepository(
    OrmRepositoryBase[
        SystemSettingEntity, 
        SystemSettingProps, 
        SystemSettingOrmEntity,
        SystemSettingOrmMapper
    ],  
    SystemSettingRepositoryPort
):

    property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def repository(self):
        return get_args(self.__orig_bases__[0])[2]

    @property
    def mapper(self):
        return get_args(self.__orig_bases__[0])[3]
