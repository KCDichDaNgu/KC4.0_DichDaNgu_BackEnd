from infrastructure.configs.token import Scope, TokenType, Platform
from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from umongo import fields, validate

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
class TokenOrmEntity(OrmEntityBase):

    user_id = fields.UUIDField(required=True)
    platform = fields.StringField(required=True, validate=validate.OneOf(Platform.enum_values()))
    token_type = fields.StringField(required=True, validate=validate.OneOf(TokenType.enum_values()))
    access_token = fields.UUIDField(required=True, unique=True)
    refresh_token = fields.UUIDField(required=True, unique=True)
    scope = fields.ListField(fields.StringField(validate=validate.OneOf(Scope.enum_values())))
    access_expires_in = fields.IntegerField(required=True)
    refresh_expires_in = fields.IntegerField(required=True)
    revoked = fields.BooleanField(default=False)
    
    class Meta:
        collection_name = database_config.COLLECTIONS['token']['name']  
        