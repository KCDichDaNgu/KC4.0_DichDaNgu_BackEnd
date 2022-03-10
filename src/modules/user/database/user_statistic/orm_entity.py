from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from umongo import fields

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
class UserStatisticOrmEntity(OrmEntityBase):

    user_id = fields.UUIDField(required=True)
    text_translation_quota = fields.DictField(required=True)
    total_translated_text = fields.DictField(required=False)
    
    class Meta:
        collection_name = database_config.COLLECTIONS['user_statistic']['name']  