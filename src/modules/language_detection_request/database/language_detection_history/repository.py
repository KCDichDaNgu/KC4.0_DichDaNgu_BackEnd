from modules.language_detection_request.database.language_detection_history.orm_mapper import LanguageDetectionHistoryOrmMapper
from modules.language_detection_request.database.language_detection_history.orm_entity import LanguageDetectionHistoryOrmEntity
from core.ports.repository import RepositoryPort
from modules.language_detection_request.domain.entities.language_detection_history import LanguageDetectionHistoryEntity, LanguageDetectionHistoryProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

from typing import get_args

class LanguageDetectionHistoryRepositoryPort(RepositoryPort[LanguageDetectionHistoryEntity, LanguageDetectionHistoryProps]):

    pass

class LanguageDetectionHistoryRepository(
    OrmRepositoryBase[
        LanguageDetectionHistoryEntity, 
        LanguageDetectionHistoryProps, 
        LanguageDetectionHistoryOrmEntity,
        LanguageDetectionHistoryOrmMapper
    ], 
    LanguageDetectionHistoryRepositoryPort
):
    
    @property
    def entity_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    @property
    def repository(self):
        return get_args(self.__orig_bases__[0])[2]

    @property
    def mapper(self):
        return get_args(self.__orig_bases__[0])[3]
