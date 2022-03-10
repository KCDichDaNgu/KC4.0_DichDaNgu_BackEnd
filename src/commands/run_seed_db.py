import asyncio
from modules.user.database.seeding.admin_account_seeder import AdminAccountSeeder
from commands import cli, click
from infrastructure.configs import EnvStateEnum
from modules.system_setting.database.seeding.system_setting_seeder import SystemSettingSeeder

from infrastructure.configs.database import MongoDBDatabase

from motor.motor_asyncio import AsyncIOMotorClient

mongodb_collections = MongoDBDatabase(
    DATABASE_NAME='translation-tool',
    PASSWORD='',
    USER='',
    HOST='localhost',
    PORT=27017,
    REPLICASET='rs0',
    CONN_OPTS={"MIN_POOL_SIZE": 10, "MAX_POOL_SIZE": 50}
).COLLECTIONS

@cli.command('run-seed-db')
@click.option('-e', '--env', default='dev', type=click.Choice(EnvStateEnum.enum_values()))
@click.option('-dbh', '--db-host', default='localhost', type=str)
@click.option('-dbp', '--db-port', default=27017, type=int)
@click.option('-dbn', '--db-name', default='translation-tool', type=str)
@click.option('-rls', '--replica-set', default='rs0', type=str)
@click.option('-drop-db', '--drop-db', default=True, type=bool)
def run_seed_db(
    env,
    db_host,
    db_port,
    db_name,
    replica_set,
    drop_db
):
    
    mongodb_uri = 'mongodb://{}:{}/{}?replicaSet={}'.format(
        db_host,
        db_port,
        db_name,
        replica_set
    )

    database_name = 'translation-tool'

    asyncio.run(create_data(
        mongodb_uri=mongodb_uri,
        database_name=database_name,
        drop_db=drop_db
    ))


async def create_data(
    mongodb_uri,
    database_name,
    drop_db
):

    db_client = AsyncIOMotorClient(mongodb_uri)

    async with await db_client.start_session() as session:

        if drop_db:
            await db_client.drop_database(database_name)

        system_setting_seeder = SystemSettingSeeder(
            db_client=db_client,
            database_name=database_name,
            collection_name=mongodb_collections['system_setting']['name']
        )

        admin_account = AdminAccountSeeder(
            db_client=db_client,
            database_name=database_name,
            collection_name=mongodb_collections['user']['name']
        )

        await system_setting_seeder.run(session)

        await admin_account.run(session)
