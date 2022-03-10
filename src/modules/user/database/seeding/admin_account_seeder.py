from core.seeder.base import BaseSeeder
from uuid import uuid4
from datetime import datetime

class AdminAccountSeeder(BaseSeeder):

    def __init__(self, db_client, collection_name, mongodb_uri = None, database_name = None) -> None:
        super().__init__(db_client, mongodb_uri, database_name)  

        self.collection_name = collection_name

        self.coll_connection = self.db[collection_name]
        self.statistic_coll_connection = self.db['user_statistic']

    async def run(self, session=None):

        saved_admin = await self.coll_connection.find_one({}, session=session)

        if not saved_admin:
            result = await self.coll_connection.insert_one({
                '_id': uuid4(),
                'username': 'admin',
                'first_name': 'super',
                'last_name': 'user',
                'avatar':'https://thumbs.dreamstime.com/b/user-avatar-line-icon-account-outline-vector-sign-linear-style-pictogram-isolated-white-admin-profile-symbol-logo-illustration-107743603.jpg',
                'email':'admin@example.com',
                'password':'12345678',
                'role':'admin',
                'status':'active',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            session=session)

            if result.inserted_id:
                await self.statistic_coll_connection.insert_one({
                    '_id': uuid4(),
                    'user_id': result.inserted_id,
                    'total_translated_text':{
                        'vi-zh': 0,
                        'vi-en': 0,
                        'vi-km': 0,
                        'vi-lo': 0,
                    },
                    'text_translation_quota':{
                        'vi-zh': 100000,
                        'vi-en': 100000,
                        'vi-km': 100000,
                        'vi-lo': 100000,
                    },
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                })
                print("Admin account seeding successfully")
            else:
                raise Exception("Admin account seeding fail")
