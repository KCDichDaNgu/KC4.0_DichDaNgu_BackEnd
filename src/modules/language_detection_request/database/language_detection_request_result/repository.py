from modules.language_detection_request.database.language_detection_request_result.orm_mapper import LanguageDetectionRequestResultOrmMapper
from modules.language_detection_request.database.language_detection_request_result.orm_entity import LanguageDetectionRequestResultOrmEntity
from core.ports.repository import RepositoryPort
from modules.language_detection_request.domain.entities.language_detection_request_result import LanguageDetectionRequestResultEntity, LanguageDetectionRequestResultProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase


from modules.task.database.task_result.repository import TasktResultRepositoryPort, TasktResultRepository

from typing import get_args

class LanguageDetectionRequestResultRepositoryPort(
    TasktResultRepositoryPort,
    RepositoryPort[
        LanguageDetectionRequestResultEntity, 
        LanguageDetectionRequestResultProps
    ]
):

    pass

class LanguageDetectionRequestResultRepository(
    TasktResultRepository,
    OrmRepositoryBase[
        LanguageDetectionRequestResultEntity, 
        LanguageDetectionRequestResultProps, 
        LanguageDetectionRequestResultOrmEntity,
        LanguageDetectionRequestResultOrmMapper
    ], 
    LanguageDetectionRequestResultRepositoryPort
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
