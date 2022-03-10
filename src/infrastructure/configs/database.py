from typing import Any, Dict
from pydantic import BaseModel, Field

class KeySpaceConfig(BaseModel):

    NAME: str = Field(None)

    DURABLE_WRITES: bool = True
    STRATEGY_CLASS: str = 'SimpleStrategy'
    STRATEGY_OPTIONS: dict = {'replication_factor': 1}
    CONNECTIONS: Any = None

class CassandraDatabase(BaseModel):

    NAME: str = Field(None)
    PASSWORD: str = Field(None)
    USER: str = Field(None)
    HOST: str = Field(None)

    SCHEMA_VERSION = 1

    KEYSPACE: KeySpaceConfig

    PROTOCOL_VERSION: int = 3

    TABLES: dict = {}

class MongoDBConnectionOptions(BaseModel):

    MIN_POOL_SIZE: int = Field(...)
    MAX_POOL_SIZE: int = Field(...)

class MongoDBDatabase(BaseModel):

    DATABASE_NAME: str = Field(...)
    PASSWORD: str = Field(...)

    USER: str = Field(...)
    HOST: str = Field(...)
    PORT: int = Field(...)

    REPLICASET: str = Field(...)

    CONN_OPTS: MongoDBConnectionOptions

    COLLECTIONS: dict = {
        "task": {
            "name": "task"
        },
        "task_result": {
            "name": "task_result"
        },
        "translation_history": {
            "name": "translation_history"
        },
        "language_detection_history": {
            "name": "language_detection_history"
        },
        "user": {
            "name": "user"
        },
        "user_statistic": {
            "name": "user_statistic"
        },
        "token": {
            "name": "token"
        },
        "system_setting": {
            "name": "system_setting"
        }
    }

    @property
    def MONGODB_URI(self):

        return 'mongodb://{}:{}/{}?replicaSet={}'.format(
            # self.USER,
            # self.PASSWORD,
            self.HOST,
            self.PORT,
            self.DATABASE_NAME,
            self.REPLICASET
        )

ORM_VALID_CLASSNAMES = [
    'OrmEntityBase',

    'TaskOrmEntity',
    'TaskResultOrmEntity',

    'TranslationHistoryOrmEntity',
    'TranslationRequestOrmEntity',
    'TranslationRequestResultOrmEntity',

    'LanguageDetectionHistoryOrmEntity',
    'LanguageDetectionRequestOrmEntity',
    'LanguageDetectionRequestResultOrmEntity',

    'UserOrmEntity'
]


def validate_orm_class_name(doc_class, class_names=ORM_VALID_CLASSNAMES):

    if not doc_class.__name__ in class_names:
        raise Exception('Orm classname changed!!! Please carefully with Parent - Child class pairs, they use class name for discriminating')

    return doc_class
