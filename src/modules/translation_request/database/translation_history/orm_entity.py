from infrastructure.configs.translation_history import TranslationHistoryTypeEnum, TranslationHistoryStatus
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf
from infrastructure.configs.main import get_mongodb_instance
from umongo import fields, validate

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
class TranslationHistoryOrmEntity(OrmEntityBase):

    creator_id = fields.UUIDField(default=None)
    task_id = fields.UUIDField(required=True)

    translation_type = fields.StringField(
        required=True, 
        validate=validate.OneOf(TranslationHistoryTypeEnum.enum_values())
    )

    status = fields.StringField(
        required=True, 
        validate=validate.OneOf(TranslationHistoryStatus.enum_values())
    )

    file_path = fields.StringField(allow_none=True)

    class Meta:
        collection_name = database_config.COLLECTIONS['translation_history']['name']

    def pre_insert(self):

        super(TranslationHistoryOrmEntity, self).pre_insert()
        
        if self.file_path is None:

            raise Exception('File path cannot be None')

    def pre_update(self):

        super(TranslationHistoryOrmEntity, self).pre_update()
        
        if self.file_path is None:

            raise Exception('File path cannot be None')
