from infrastructure.configs.main import MongoDBDatabase, GlobalConfig, get_cnf, get_mongodb_instance
from infrastructure.configs.database import validate_orm_class_name
from modules.task.database.task_result.orm_entity import TaskResultOrmEntity

config: GlobalConfig = get_cnf()
database_config: MongoDBDatabase = config.MONGODB_DATABASE

db_instance = get_mongodb_instance()

@db_instance.register
@validate_orm_class_name
class TranslationRequestResultOrmEntity(TaskResultOrmEntity):
    
    def pre_insert(self):

        super(TranslationRequestResultOrmEntity, self).pre_insert()

    def pre_update(self):

        super(TranslationRequestResultOrmEntity, self).pre_update()
