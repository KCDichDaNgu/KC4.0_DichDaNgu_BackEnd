from asyncio.coroutines import iscoroutine
from typing import List
from umongo.exceptions import DeleteError, NotCreatedError
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument
from umongo.query_mapper import map_query
from infrastructure.configs.main import get_mongodb_instance
from uuid import uuid4
from datetime import datetime

from umongo.frameworks.tools import cook_find_filter

from umongo import Document, fields
db_instance = get_mongodb_instance()

@db_instance.register
class OrmEntityBase(Document):

    id = fields.UUIDField(unique=True, required=True, attribute='_id')
    created_at = fields.DateTimeField(allow_none=True)
    updated_at = fields.DateTimeField(allow_none=True)

    class Meta:
        abstract = True
        indexes = ['-created_at']

    def pre_insert(self):

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @classmethod
    def get_table_name(cls):
        return cls.collection

    @classmethod
    async def coroutined_pre_insert(cls, document: MotorAsyncIODocument):
        
        ret = document.pre_insert()

        if iscoroutine(ret):
            ret = await ret

        return ret

    @classmethod
    async def coroutined_pre_update(cls, document: MotorAsyncIODocument):

        ret = document.pre_update()

        if iscoroutine(ret):
            ret = await ret

        return ret

    @classmethod
    async def coroutined_pre_delete(cls, document: MotorAsyncIODocument):

        ret = document.pre_delete()

        if iscoroutine(ret):
            ret = await ret

        return ret

    @classmethod
    async def coroutined_post_insert(cls, document: MotorAsyncIODocument, ret):

        ret = document.post_insert(ret)

        if iscoroutine(ret):
            ret = await ret

        return ret

    @classmethod
    async def coroutined_post_update(cls, document: MotorAsyncIODocument, ret):

        ret = document.post_update(ret)

        if iscoroutine(ret):
            ret = await ret

        return ret

    @classmethod
    async def coroutined_post_delete(cls, document: MotorAsyncIODocument, ret):

        ret = document.post_delete(ret)

        if iscoroutine(ret):
            ret = await ret

        return ret
        
    @classmethod
    async def insert_many(cls, documents: List[MotorAsyncIODocument], io_validate_all=False):

        async with db_instance.session() as session:
            async with session.start_transaction():

                collection = cls.get_table_name()

                payloads = []

                for document in documents:

                    await cls.coroutined_pre_insert(document)

                    document.required_validate()

                    await document.io_validate(validate_all=io_validate_all)


                payloads = [document._data.to_mongo(update=False) for document in documents]
                
                from umongo.frameworks.motor_asyncio import SESSION

                ret = await collection.insert_many(payloads, session=SESSION.get())

                # TODO: check ret ?
                for index, document in enumerate(documents):

                    document._data.set(document.pk_field, ret.inserted_ids[index])

                    document.is_created = True

                await cls.coroutined_post_insert(document, ret)

    @classmethod
    async def delete_many(cls, documents: List[MotorAsyncIODocument], conditions=None):

        async with db_instance.session() as session:
            async with session.start_transaction():

                collection = cls.get_table_name()
                list_subquery = []

                for document in documents:
                
                    if not document.is_created:
                        raise NotCreatedError("Document doesn't exists in database")

                    subquery = conditions or {}

                    subquery['_id'] = document.pk

                    # pre_delete can provide additional query filter
                    additional_filter = await cls.coroutined_pre_delete(document)

                    if additional_filter:
                        subquery.update(map_query(additional_filter, document.schema.fields))

                    list_subquery.append(subquery)

                query = {
                    '$or': list_subquery
                }

                from umongo.frameworks.motor_asyncio import SESSION

                ret = await collection.delete_many(query, session=SESSION.get())

                if ret.deleted_count != len(documents):
                    raise DeleteError(ret)

                for document in documents:

                    document.is_created = False

                    await cls.coroutined_post_delete(document, ret)

                return ret
