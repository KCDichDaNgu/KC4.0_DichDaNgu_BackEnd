from infrastructure.configs.translation_task import AllowedFileTranslationExtensionEnum
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.database import validate_orm_class_name
from umongo import validate, fields
from typing import Optional

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE

db_instance = get_mongodb_instance()

@db_instance.register
@validate_orm_class_name
class TaskResultOrmEntity(OrmEntityBase):

    task_id = fields.UUIDField(required=True)

    step = fields.StringField(required=True)

    file_path = fields.StringField(allow_none=True)

    class Meta:
        collection_name = database_config.COLLECTIONS['task_result']['name']

    def pre_insert(self):

        super(TaskResultOrmEntity, self).pre_insert()
        
        if self.file_path is None:

            raise Exception('File path cannot be None')

    def pre_update(self):

        super(TaskResultOrmEntity, self).pre_update()
        
        if self.file_path is None:

            raise Exception('File path cannot be None')
