from typing import get_args
from modules.task.database.task_result.orm_mapper import TaskResultOrmMapper
from modules.task.database.task_result.orm_entity import TaskResultOrmEntity
from core.ports.repository import RepositoryPort
from modules.task.domain.entities.task_result import TaskResultEntity, TaskResultProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

class TasktResultRepositoryPort(
    RepositoryPort[
        TaskResultEntity, 
        TaskResultProps
    ]):

    pass

class TasktResultRepository(
    OrmRepositoryBase[
        TaskResultEntity, 
        TaskResultProps, 
        TaskResultOrmEntity,
        TaskResultOrmMapper
    ], 
    TasktResultRepositoryPort
):

    @property
    # @abstractmethod
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    # @abstractmethod
    def repository(self):
        return get_args(self.__orig_bases__[0])[2]

    @property
    # @abstractmethod
    def mapper(self):
        return get_args(self.__orig_bases__[0])[3]

    pass
