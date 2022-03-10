import asyncio
from infrastructure.configs.database import MongoDBDatabase
from infrastructure.configs.main import update_mongodb_instance
from cassandra.cqlengine import connection
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.management import _create_keyspace
from infrastructure.configs.main import CassandraDatabase
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance

def init_cassandra_db(cassandraDbConfig: CassandraDatabase):

    from infrastructure.database.base_classes.cassandra.aiocqlengine.session import aiosession_for_cqlengine

    from modules.translation_request.database.translation_request.orm_entity import TranslationRequestOrmEntity
    from modules.translation_request.database.translation_request_result.orm_entity import TranslationRequestResultOrmEntity
    from modules.translation_request.database.translation_history.orm_entity import TranslationHistoryOrmEntity

    auth_provider = PlainTextAuthProvider(
        username=cassandraDbConfig.USER,
        password=cassandraDbConfig.PASSWORD
    )

    connection.setup(
        hosts=[cassandraDbConfig.HOST],
        default_keyspace=cassandraDbConfig.KEYSPACE.NAME,
        auth_provider=auth_provider,
        protocol_version=cassandraDbConfig.PROTOCOL_VERSION
    )
    
    _create_keyspace(
        name=cassandraDbConfig.KEYSPACE.NAME, 
        durable_writes=cassandraDbConfig.KEYSPACE.DURABLE_WRITES, 
        strategy_class=cassandraDbConfig.KEYSPACE.STRATEGY_CLASS,
        strategy_options=cassandraDbConfig.KEYSPACE.STRATEGY_OPTIONS, 
        connections=cassandraDbConfig.KEYSPACE.CONNECTIONS
    )

    current_session = connection.session

    current_session.set_keyspace(cassandraDbConfig.KEYSPACE.NAME)
    
    aiosession_for_cqlengine(current_session)
    
    connection.set_session(current_session)

    # TranslationRequestOrmEntity.sync_table_to_db(
    #     keyspaces=[cassandraDbConfig.KEYSPACE.NAME]
    # )
    
    # TranslationRequestResultOrmEntity.sync_table_to_db(
    #     keyspaces=[cassandraDbConfig.KEYSPACE.NAME]
    # )
    
    # TranslationHistoryOrmEntity.sync_table_to_db(
    #     keyspaces=[cassandraDbConfig.KEYSPACE.NAME]
    # )

def init_mongodb(mongodbConfig: MongoDBDatabase):

    conn_opts = {}

    if mongodbConfig.CONN_OPTS.MIN_POOL_SIZE:

        conn_opts.update(minPoolSize=mongodbConfig.CONN_OPTS.MIN_POOL_SIZE)

    if mongodbConfig.CONN_OPTS.MAX_POOL_SIZE:

        conn_opts.update(minPoolSize=mongodbConfig.CONN_OPTS.MAX_POOL_SIZE)

    # db = MongoClient(
    #     mongodbConfig.MONGODB_URI, 
    #     **conn_opts
    # )[mongodbConfig.DATABASE_NAME]

    # instance = PyMongoInstance(db)

    db = AsyncIOMotorClient(
        mongodbConfig.MONGODB_URI, 
        **conn_opts
    )[mongodbConfig.DATABASE_NAME]

    instance = MotorAsyncIOInstance(db)
    
    update_mongodb_instance(instance)
