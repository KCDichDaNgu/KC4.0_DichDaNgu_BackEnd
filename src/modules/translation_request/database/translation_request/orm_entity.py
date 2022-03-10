from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf
from infrastructure.configs.task import (
    TRANSLATION_PRIVATE_TASKS,
)
from infrastructure.configs.database import validate_orm_class_name
from umongo import fields, validate
from infrastructure.configs.main import get_mongodb_instance
from modules.task.database.task.orm_entity import TaskOrmEntity
from infrastructure.configs.task import TranslationTaskNameEnum, TaskTypeEnum

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
@validate_orm_class_name
class TranslationRequestOrmEntity(TaskOrmEntity):

    task_name = fields.StringField(
        required=True, 
        validate=validate.OneOf(TranslationTaskNameEnum.enum_values())
    )
    
    receiver_email = fields.EmailField(
        allow_none=True
    )
    
    total_email_sent = fields.IntegerField(
        allow_none=True,
        default=0,
        validate=validate.Range(min=0)
    )
    
    num_chars = fields.IntegerField(
        allow_none=False,
        default=0, 
        validate=validate.Range(min=0)
    )

    def pre_insert(self):
        
        super(TranslationRequestOrmEntity, self).pre_insert()

        if self.task_name in TRANSLATION_PRIVATE_TASKS and not self.creator_id:

            raise Exception('Creator cannot be None')
