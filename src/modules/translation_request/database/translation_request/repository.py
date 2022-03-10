from modules.translation_request.database.translation_request.orm_mapper import TranslationRequestOrmMapper
from modules.translation_request.database.translation_request.orm_entity import TranslationRequestOrmEntity
from core.ports.repository import RepositoryPort
from modules.translation_request.domain.entities.translation_request import TranslationRequestEntity, TranslationRequestProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

from modules.task.database.task.repository import TaskRepository, TaskRepositoryPort

from typing import get_args

class TranslationRequestRepositoryPort(
    TaskRepositoryPort,
    RepositoryPort[
        TranslationRequestEntity, 
        TranslationRequestProps
    ]
):

    pass

class TranslationRequestRepository(
    TaskRepository,
    OrmRepositoryBase[
        TranslationRequestEntity, 
        TranslationRequestProps, 
        TranslationRequestOrmEntity,
        TranslationRequestOrmMapper
    ], 
    TranslationRequestRepositoryPort
):

    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[1])[0]

    @property
    def repository(self):
        return get_args(self.__orig_bases__[1])[2]

    @property
    def mapper(self):
        return get_args(self.__orig_bases__[1])[3]
