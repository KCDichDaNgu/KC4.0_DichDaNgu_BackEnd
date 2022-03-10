from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorClient

class BaseSeeder(ABC):

    def __init__(self, db_client, mongodb_uri, database_name) -> None:

        self.mongodb_uri = mongodb_uri
        self.database_name = database_name

        if db_client:
            self.db_client = db_client
        else:
            self.db_client = AsyncIOMotorClient(
                self.mongodb_uri
            )

        self.db = self.db_client[self.database_name]

    @abstractmethod
    def run(self):
        ...
