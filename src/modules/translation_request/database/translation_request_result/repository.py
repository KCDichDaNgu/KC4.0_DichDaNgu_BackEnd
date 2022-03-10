from modules.translation_request.database.translation_request_result.orm_mapper import TranslationRequestResultOrmMapper
from modules.translation_request.database.translation_request_result.orm_entity import TranslationRequestResultOrmEntity
from core.ports.repository import RepositoryPort
from modules.translation_request.domain.entities.translation_request_result import TranslationRequestResultEntity, TranslationRequestResultProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase


from modules.task.database.task_result.repository import TasktResultRepositoryPort, TasktResultRepository

from typing import get_args

class TranslationRequestResultRepositoryPort(
    TasktResultRepositoryPort,
    RepositoryPort[
        TranslationRequestResultEntity, 
        TranslationRequestResultProps
    ]
):

    pass

class TranslationRequestResultRepository(
    TasktResultRepository,
    OrmRepositoryBase[
        TranslationRequestResultEntity, 
        TranslationRequestResultProps, 
        TranslationRequestResultOrmEntity,
        TranslationRequestResultOrmMapper
    ], 
    TranslationRequestResultRepositoryPort
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
