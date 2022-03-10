from modules.task.database.task.orm_mapper import TaskOrmMapper
from modules.task.database.task.orm_entity import TaskOrmEntity
from core.ports.repository import RepositoryPort
from abc import abstractmethod
from typing import get_args
from modules.task.domain.entities.task import TaskEntity, TaskProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

class TaskRepositoryPort(RepositoryPort[TaskEntity, TaskProps]):

    pass

class TaskRepository(
    OrmRepositoryBase[
        TaskEntity, 
        TaskProps, 
        TaskOrmEntity,
        TaskOrmMapper
    ], 
    TaskRepositoryPort
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
