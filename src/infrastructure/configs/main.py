from pathlib import Path
from pydantic import Field, BaseSettings, BaseModel

from typing import Any, Dict, Optional, Union
from enum import unique

from pydantic.networks import AnyHttpUrl
from umongo.frameworks import MotorAsyncIOInstance, PyMongoInstance
from core.types import ExtendedEnum

from infrastructure.configs.database import CassandraDatabase, MongoDBDatabase
from infrastructure.configs.event_dispatcher import KafkaConsumer, KafkaProducer

import os


@unique
class EnvStateEnum(str, ExtendedEnum):

    dev = "dev"
    prod = "prod"


@unique
class ServerTypeEnum(str, ExtendedEnum):

    uvicorn = "uvicorn"
    built_in = "built_in"


@unique
class StatusCodeEnum(int, ExtendedEnum):

    success = 1
    failed = 0


@unique
class BackgroundTaskTriggerEnum(str, ExtendedEnum):

    interval = "interval"
    cron = "cron"
    date = "date"


class BackgroundTask(BaseModel):

    ID: str
    TRIGGER: BackgroundTaskTriggerEnum
    CONFIG: Dict

    class Config:
        use_enum_values = True


class AppConfig(BaseModel):

    APP_NAME: str = "translation-backend"

    STATIC_FOLDER: str = "static"

    ROUTES: Dict = {
        "translation_request": {
            "path": "/",
            "name": "Translation request",
            "abstract": True,
        },
        "translation_request.update_receiver_email": {
            "path": "update-receiver-email",
            "name": "update_receiver_email",
            "summary": "update_receiver_email",
            "desc": "update_receiver_email",
            "method": "PUT",
            "abstract": False,
        },
        "translation_request.text_translation.create": {
            "path": "translate",
            "name": "Create text translation request",
            "summary": "Create text translation request",
            "desc": "Create text translation request",
            "method": "POST",
            "abstract": False,
        },
        "translation_request.doc_translation.create": {
            "path": "translate_f",
            "name": "Create document translation request",
            "summary": "Create document translation request",
            "desc": "Create document translation request",
            "method": "POST",
            "abstract": False,
        },
        "translation_history": {
            "path": "/translation-history",
            "name": "Translation History",
            "abstract": True,
        },
        "translation_history.get_single": {
            "path": "/get-single",
            "name": "Get single translation history",
            "summary": "Get single translation history",
            "desc": "Get single translation history",
            "method": "GET",
            "abstract": False,
        },
        "translation_history.list": {
            "path": "",
            "name": "Get many translation history",
            "summary": "Get many translation history",
            "desc": "Get many translation history",
            "method": "GET",
            "abstract": False,
        },
        "language_detection_request": {
            "path": "/",
            "name": "Language detection request",
            "abstract": True,
        },
        "language_detection_request.text_language_detection.create": {
            "path": "detect-lang",
            "name": "Create text language detection request",
            "summary": "Create text language detection request",
            "desc": "Create text language detection request",
            "method": "POST",
            "abstract": False,
        },
        "language_detection_request.doc_language_detection.create": {
            "path": "detect-f-lang",
            "name": "Create document language detection request",
            "summary": "Create document language detection request",
            "desc": "Create document language detection request",
            "method": "POST",
            "abstract": False,
        },
        "language_detection_history": {
            "path": "/lang-detection-history",
            "name": "Language detection history",
            "abstract": True,
        },
        "language_detection_history.get_single": {
            "path": "/get-single",
            "name": "Get single language detection history",
            "summary": "Get single language detection history",
            "desc": "Get single language detection history",
            "method": "GET",
            "abstract": False,
        },
        "static_files": {
            "path": "/static",
            "name": "Static files serving",
            "abstract": False,
        },
        "user": {"path": "/user", "name": "User routes", "abstract": True},
        "user.auth": {
            "path": "/auth",
            "name": "Authentication",
            "summary": "Provider access token via Google access code or refresh token",
            "desc": "Provider access token via Google access code or refresh token",
            "method": "POST",
            "abstract": False,
        },
        "user.logout": {
            "path": "/logout",
            "name": "Logout",
            "summary": "Logout from system",
            "desc": "Logout from system",
            "method": "POST",
            "abstract": False,
        },
        "user.login": {
            "path": "/login",
            "name": "Login",
            "summary": "Login into system",
            "desc": "Login into system",
            "method": "POST",
            "abstract": False,
        },
        "user.me": {
            "path": "/me",
            "name": "User information",
            "summary": "Users get information of themselves",
            "desc": "Users get information of themselves",
            "method": "GET",
            "abstract": False,
        },
        "user.get": {
            "path": "/",
            "name": "User information",
            "summary": "Users get information",
            "desc": "Users get information",
            "method": "GET",
            "abstract": False,
        },
        "user.update_self": {
            "path": "/",
            "name": "User self updating",
            "summary": "Users update their information",
            "desc": "Users update their information",
            "method": "PUT",
            "abstract": False,
        },
        "user.update_other": {
            "path": "/other",
            "name": "Updating other user",
            "summary": "Users update other information",
            "desc": "Users update other information",
            "method": "PUT",
            "abstract": False,
        },
        "user.get_list": {
            "path": "/search",
            "name": "Seaching user",
            "summary": "Get users by conditions",
            "desc": "Get users by conditions",
            "method": "GET",
            "abstract": False,
        },
        "admin": {"path": "/admin", "name": "Admin routes", "abstract": True},
        "admin.create_user": {
            "path": "/user",
            "name": "Create user",
            "summary": "Create new user",
            "desc": "Create new user",
            "method": "Post",
            "abstract": False,
        },
        "admin.update_user_quota": {
            "path": "/user/update_quota",
            "name": "Update user quota",
            "summary": "Update user quota",
            "desc": "Update user quota",
            "method": "Post",
            "abstract": False,
        },
        "system_setting": {
            "path": "/system-setting",
            "name": "System setting",
            "abstract": True,
        },
        "system_setting.update": {
            "path": "",
            "name": "Update system setting",
            "summary": "Update system setting",
            "desc": "Update system setting",
            "method": "PUT",
            "abstract": False,
        },
        "system_setting.get": {
            "path": "",
            "name": "Get system setting",
            "summary": "Get system setting",
            "desc": "Get system setting",
            "method": "GET",
            "abstract": False,
        },
    }

    API_BASEPATH: str = "/api"
    API_VERSION: str = "0.0.1"

    STRICT_SLASHES = False

    BACKGROUND_TASKS: Dict[str, BackgroundTask] = {
        "delete_invalid_file": BackgroundTask(
            ID="delete_invalid_file",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        
        "delete_invalid_task": BackgroundTask(
            ID="delete_invalid_task",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        
         "send_translation_email": BackgroundTask(
            ID="send_translation_email",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        

        "detect_plain_text_language_created_by_public_request": BackgroundTask(
            ID="detect_plain_text_language_created_by_public_request",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "detect_file_language_created_by_public_request": BackgroundTask(
            ID="detect_file_language_created_by_public_request",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        
        
        "detect_plain_text_language_created_by_private_request": BackgroundTask(
            ID="detect_plain_text_language_created_by_private_request",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "detect_file_language_created_by_private_request": BackgroundTask(
            ID="detect_file_language_created_by_private_request",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        
        
        "translate_file_created_by_private_request.detect_content_language": BackgroundTask(
            ID="translate_file_created_by_private_request.detect_content_language",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "translate_file_created_by_private_request.translate_content.docx": BackgroundTask(
            ID="translate_file_created_by_private_request.translate_content.docx",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "translate_file_created_by_private_request.translate_content.pptx": BackgroundTask(
            ID="translate_file_created_by_private_request.translate_content.pptx",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "translate_file_created_by_private_request.translate_content.txt": BackgroundTask(
            ID="translate_file_created_by_private_request.translate_content.txt",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "translate_file_created_by_private_request.translate_content.xlsx": BackgroundTask(
            ID="translate_file_created_by_private_request.translate_content.xlsx",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        
        
        
        "translate_file_created_by_public_request.detect_content_language": BackgroundTask(
            ID="translate_file_created_by_public_request.detect_content_language",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "translate_file_created_by_public_request.translate_content.docx": BackgroundTask(
            ID="translate_file_created_by_public_request.translate_content.docx",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "translate_file_created_by_public_request.translate_content.pptx": BackgroundTask(
            ID="translate_file_created_by_public_request.translate_content.pptx",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "translate_file_created_by_public_request.translate_content.txt": BackgroundTask(
            ID="translate_file_created_by_public_request.translate_content.txt",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "translate_file_created_by_public_request.translate_content.xlsx": BackgroundTask(
            ID="translate_file_created_by_public_request.translate_content.xlsx",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        
        
        
        "translate_plain_text_created_by_private_request.detect_content_language": BackgroundTask(
            ID="translate_plain_text_created_by_private_request.detect_content_language",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "translate_plain_text_created_by_private_request.translate_content": BackgroundTask(
            ID="translate_plain_text_created_by_private_request.translate_content",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        
        
        
        "translate_plain_text_created_by_public_request.detect_content_language": BackgroundTask(
            ID="translate_plain_text_created_by_public_request.detect_content_language",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
        "translate_plain_text_created_by_public_request.translate_content": BackgroundTask(
            ID="translate_plain_text_created_by_public_request.translate_content",
            TRIGGER=BackgroundTaskTriggerEnum.interval.value,
            CONFIG=dict(seconds=0, max_instances=1),
        ),
    }

    MAX_QUERY_SIZE = 10


class TranslationAPI(BaseModel):

    URL: AnyHttpUrl = Field(...)
    METHOD: str = Field(...)
    ALLOWED_CONCURRENT_REQUEST: int = Field(...)


class LanguageDetectionAPI(BaseModel):

    URL: AnyHttpUrl = Field(...)
    METHOD: str = Field(...)
    ALLOWED_CONCURRENT_REQUEST: int = Field(...)

class Pagination(BaseModel):

    MAX_PER_PAGE = 10
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 5


class Oauth2ProviderAPI(BaseModel):

    NAME: str = Field(...)
    URL: AnyHttpUrl = Field(...)
    METHOD: str = Field(...)


class Oauth2Provider(BaseModel):

    GOOGLE: Oauth2ProviderAPI = Field(...)


class GlobalConfig(BaseSettings):

    """Global configurations."""

    APP_CONFIG: AppConfig = AppConfig()

    # define global variables with the Field class
    ENV_STATE: Optional[EnvStateEnum] = EnvStateEnum.dev.value

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_DEBUG: bool = False
    APP_WORKERS: int = 1
    ACCESS_LOG: bool = False
    SSL_KEYFILE: str = None
    SSL_CERTFILE: str = None
    APP_LIFESPAN: str = None
    SERVER_TYPE: str = None

    CQLENG_ALLOW_SCHEMA_MANAGEMENT: Any = Field(env="CQLENG_ALLOW_SCHEMA_MANAGEMENT")

    CASSANDRA_DATABASE: CassandraDatabase
    MONGODB_DATABASE: MongoDBDatabase

    KAFKA_CONSUMER: KafkaConsumer
    KAFKA_PRODUCER: KafkaProducer

    PRIVATE_TRANSLATION_API: TranslationAPI
    PRIVATE_LANGUAGE_DETECTION_API: LanguageDetectionAPI

    PUBLIC_TRANSLATION_API: TranslationAPI
    PUBLIC_LANGUAGE_DETECTION_API: LanguageDetectionAPI

    OAUTH2_PROVIDER: Oauth2Provider
    ACCESS_TOKEN_TTL: int
    REFRESH_TOKEN_TTL: int
    PAGINATION: Pagination = Pagination()

    class Config:
        """Loads the dotenv file."""

        env_file = ".env"
        env_prefix = "SANIC_"
        env_file_encoding = "utf-8"

    def _build_values(
        self,
        init_kwargs: Dict[str, Any],
        _env_file: Union[Path, str, None],
        _env_file_encoding: Optional[str],
        _secrets_dir: Union[Path, str, None],
    ) -> Dict[str, Any]:

        if os.getenv("CQLENG_ALLOW_SCHEMA_MANAGEMENT") is None:
            os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"

        return super()._build_values(
            init_kwargs,
            _env_file=_env_file,
            _env_file_encoding=_env_file_encoding,
            _secrets_dir=_secrets_dir,
        )


class DevConfig(GlobalConfig):
    """Development configurations."""

    APP_DEBUG = True

    class Config:
        env_file = ".env.development"


class ProdConfig(GlobalConfig):
    """Production configurations."""

    APP_DEBUG = False

    class Config:
        env_file = ".env.production"


def update_cnf(new_config):

    ConfigStore.GLOBAL_CNF = new_config

    return ConfigStore.GLOBAL_CNF


def get_cnf() -> GlobalConfig:

    return ConfigStore.GLOBAL_CNF


def update_mongodb_instance(ins):

    ConfigStore.MONGODB_INS = ins

    return ConfigStore.MONGODB_INS


def get_mongodb_instance():

    return ConfigStore.MONGODB_INS


class ConfigStore:

    GLOBAL_CNF: GlobalConfig = None
    MONGODB_INS: Union[MotorAsyncIOInstance, PyMongoInstance] = None


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str], override_config: Optional[dict]):
        self.env_state = env_state
        self.override_config = override_config

    def __call__(self):

        config = None

        if self.env_state == EnvStateEnum.dev.value:
            config = DevConfig(**self.override_config)
            config.ENV_STATE = EnvStateEnum.dev.value

        elif self.env_state == EnvStateEnum.prod.value:
            config = ProdConfig(**self.override_config)
            config.ENV_STATE = EnvStateEnum.prod.value

        else:
            config = DevConfig(**self.override_config)
            config.ENV_STATE = EnvStateEnum.dev.value

        update_cnf(config)

        return config
