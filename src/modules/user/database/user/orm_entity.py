from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.database import validate_orm_class_name
from infrastructure.configs.user import UserStatus, UserRole
from infrastructure.database.base_classes.mongodb import OrmEntityBase
from umongo import fields, validate

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE
db_instance = get_mongodb_instance()

@db_instance.register
@validate_orm_class_name
class UserOrmEntity(OrmEntityBase):
    
    username = fields.StringField(required=True, unique=True)
    first_name = fields.StringField(required=True)
    last_name = fields.StringField(required=False)
    password = fields.StringField(required=False)
    avatar = fields.StringField(required=False)
    email = fields.StringField(required=True, unique=True)
    role = fields.StringField(required=True, validate=validate.OneOf(UserRole.enum_values()))
    status = fields.StringField(required=True, validate=validate.OneOf(UserStatus.enum_values()))

    class Meta:
        collection_name = database_config.COLLECTIONS['user']['name']
        indexes =  ({'key': ['username', 'email'], 'unique': True},)

    def pre_insert(self):
        super(UserOrmEntity, self).pre_insert()

    def pre_update(self):
        super(UserOrmEntity, self).pre_update()
