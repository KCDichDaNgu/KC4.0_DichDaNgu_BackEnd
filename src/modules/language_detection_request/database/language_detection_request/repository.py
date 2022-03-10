from modules.language_detection_request.database.language_detection_request.orm_mapper import LanguageDetectionRequestOrmMapper
from modules.language_detection_request.database.language_detection_request.orm_entity import LanguageDetectionRequestOrmEntity
from core.ports.repository import RepositoryPort
from modules.language_detection_request.domain.entities.language_detection_request import LanguageDetectionRequestEntity, LanguageDetectionRequestProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

from modules.task.database.task.repository import TaskRepository, TaskRepositoryPort

from typing import get_args

class LanguageDetectionRequestRepositoryPort(
    TaskRepositoryPort,
    RepositoryPort[
        LanguageDetectionRequestEntity, 
        LanguageDetectionRequestProps
    ]
):

    pass

class LanguageDetectionRequestRepository(
    TaskRepository,
    OrmRepositoryBase[
        LanguageDetectionRequestEntity, 
        LanguageDetectionRequestProps, 
        LanguageDetectionRequestOrmEntity,
        LanguageDetectionRequestOrmMapper
    ], 
    LanguageDetectionRequestRepositoryPort
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
