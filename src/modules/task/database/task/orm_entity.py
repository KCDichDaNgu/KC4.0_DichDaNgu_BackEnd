from datetime import timedelta

from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from infrastructure.configs.task import (
    TASK_EXPIRATION_TIME, 
    CreatorTypeEnum, 
    LanguageDetectionTaskNameEnum, 
    StepStatusEnum, 
    TranslationTaskNameEnum,
    AllowedFileTranslationExtensionEnum
)
from infrastructure.configs.database import validate_orm_class_name
from infrastructure.configs.main import get_mongodb_instance
from umongo import fields, validate

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
@validate_orm_class_name
class TaskOrmEntity(OrmEntityBase):

    creator_id = fields.UUIDField(allow_none=True)

    task_name = fields.StringField(
        required=True, 
        validate=validate.OneOf([
            *TranslationTaskNameEnum.enum_values(),
            *LanguageDetectionTaskNameEnum.enum_values()
        ])
    )

    creator_type = fields.StringField(
        required=True, 
        validate=validate.OneOf(CreatorTypeEnum.enum_values())
    )

    step_status = fields.StringField(
        required=True,
        validate=validate.OneOf(StepStatusEnum.enum_values())
    )

    current_step = fields.StringField(
        required=True
    )
    
    file_type = fields.StringField(
        allow_none=True,
        validate=validate.OneOf(AllowedFileTranslationExtensionEnum.enum_values())
    )

    # expired_date = fields.DateTimeField(required=True, allow_none=True)

    class Meta:
        collection_name = database_config.COLLECTIONS['task']['name']
    
    # def pre_insert(self):
        
    #     super(TaskOrmEntity, self).pre_insert()
        
    #     if self.created_at is not None and self.expired_date is None:
            
    #         self.expired_date = self.created_at + timedelta(seconds=TASK_EXPIRATION_TIME)
