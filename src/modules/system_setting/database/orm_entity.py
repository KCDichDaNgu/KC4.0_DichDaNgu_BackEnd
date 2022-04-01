from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf
from infrastructure.configs.main import get_mongodb_instance
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from umongo import fields, validate

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
class SystemSettingOrmEntity(OrmEntityBase):

    editor_id = fields.UUIDField(allow_none=True)
    # max_user_text_translation_per_day = fields.IntegerField(required=True)
    # max_user_doc_translation_per_day = fields.IntegerField(required=True)
    task_expired_duration = fields.FloatField(required=True)
    
    translation_api_url = fields.UrlField(allow_none=True, default="http://nmtuet.ddns.net:1710/translate_paragraphs") 
    translation_api_allowed_concurrent_req = fields.IntegerField(allow_none=False, default=1)
    
    language_detection_api_url = fields.UrlField(allow_none=True, default="http://nmtuet.ddns.net:1820/detect_lang") 
    language_detection_api_allowed_concurrent_req = fields.IntegerField(allow_none=False, default=1)
    
    translation_speed_for_each_character = fields.FloatField(allow_none=False, default=0.05)
    language_detection_speed = fields.FloatField(allow_none=False, default=0.05)
    
    email_for_sending_email = fields.EmailField(required=True)
    email_password_for_sending_email = fields.StringField(required=True)
    
    allowed_total_chars_for_text_translation = fields.IntegerField(allow_none=False, default=5000)
    allowed_file_size_in_mb_for_file_translation = fields.FloatField(allow_none=False, default=1.0)
    
    class Meta:
        collection_name = database_config.COLLECTIONS['system_setting']['name']

    def pre_insert(self):
        super(SystemSettingOrmEntity, self).pre_insert()

    def pre_update(self):

        super(SystemSettingOrmEntity, self).pre_update()
