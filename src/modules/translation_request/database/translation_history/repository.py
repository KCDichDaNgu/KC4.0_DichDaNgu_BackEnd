from modules.translation_request.database.translation_history.orm_mapper import TranslationHistoryOrmMapper
from modules.translation_request.database.translation_history.orm_entity import TranslationHistoryOrmEntity
from core.ports.repository import RepositoryPort
from modules.translation_request.domain.entities.translation_history import TranslationHistoryEntity, TranslationHistoryProps
from infrastructure.database.base_classes.mongodb.orm_repository_base import OrmRepositoryBase

from typing import get_args

class TranslationHistoryRepositoryPort(RepositoryPort[TranslationHistoryEntity, TranslationHistoryProps]):

    pass

class TranslationHistoryRepository(
    OrmRepositoryBase[
        TranslationHistoryEntity, 
        TranslationHistoryProps, 
        TranslationHistoryOrmEntity,
        TranslationHistoryOrmMapper
    ], 
    TranslationHistoryRepositoryPort
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
