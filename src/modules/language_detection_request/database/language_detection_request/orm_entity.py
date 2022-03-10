from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf
from infrastructure.configs.task import (
    LANGUAGE_DETECTION_PRIVATE_TASKS
)
from infrastructure.configs.database import validate_orm_class_name
from umongo import fields, validate
from infrastructure.configs.main import get_mongodb_instance
from modules.task.database.task.orm_entity import TaskOrmEntity
from infrastructure.configs.task import LanguageDetectionTaskNameEnum

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
@validate_orm_class_name
class LanguageDetectionRequestOrmEntity(TaskOrmEntity):

    task_name = fields.StringField(
        required=True, 
        validate=validate.OneOf(LanguageDetectionTaskNameEnum.enum_values())
    )

    def pre_insert(self):
        
        super(LanguageDetectionRequestOrmEntity, self).pre_insert()

        if self.task_name in LANGUAGE_DETECTION_PRIVATE_TASKS and not self.creator_id:

            raise Exception('Creator cannot be None')
