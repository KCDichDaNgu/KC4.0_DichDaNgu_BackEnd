import asyncio
from inspect import iscoroutine
from typing import List
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument
from umongo.exceptions import NotCreatedError, DeleteError
from umongo.query_mapper import map_query
from infrastructure.configs.main import get_mongodb_instance

db_instance = get_mongodb_instance()

async def coroutined_pre_insert(document: MotorAsyncIODocument):
    ret = document.pre_insert()
    if iscoroutine(ret):
        ret = await ret
    return ret

async def coroutined_pre_update(document: MotorAsyncIODocument):
    ret = document.pre_update()
    if iscoroutine(ret):
        ret = await ret
    return ret

async def coroutined_pre_delete(document: MotorAsyncIODocument):
    ret = document.pre_delete()
    if iscoroutine(ret):
        ret = await ret
    return ret

async def coroutined_post_insert(document: MotorAsyncIODocument, ret):
    ret = document.post_insert(ret)
    if iscoroutine(ret):
        ret = await ret
    return ret

async def coroutined_post_update(document: MotorAsyncIODocument, ret):
    ret = document.post_update(ret)
    if iscoroutine(ret):
        ret = await ret
    return ret

async def coroutined_post_delete(document: MotorAsyncIODocument, ret):
    ret = document.post_delete(ret)
    if iscoroutine(ret):
        ret = await ret
    return ret


async def insert_many(documents: List[MotorAsyncIODocument], io_validate_all=False):

    async with db_instance.session() as session:
        async with session.start_transaction():

            collection = documents[0].collection

            payloads = []

            for document in documents:

                await coroutined_pre_insert(document)

                document.required_validate()

                await document.io_validate(validate_all=io_validate_all)

            payloads = [document._data.to_mongo(update=False) for document in documents]
            
            from umongo.frameworks.motor_asyncio import SESSION

            ret = await collection.insert_many(payloads, session=SESSION.get())

            # TODO: check ret ?
            for index, document in enumerate(documents):

                document._data.set(document.pk_field, ret.inserted_ids[index])

                document.is_created = True

                await coroutined_post_insert(document, ret)


async def update_many(documents: List[MotorAsyncIODocument], io_validate_all=False, replace=False):
    ...

async def delete_many(documents: List[MotorAsyncIODocument], conditions=None):

    async with db_instance.session() as session:
        async with session.start_transaction():

            collection = documents[0].collection

            list_subquery = []

            for document in documents:
            
                if not document.is_created:
                    raise NotCreatedError("Document doesn't exists in database")

                subquery = conditions or {}

                subquery['_id'] = document.pk

                # pre_delete can provide additional query filter
                additional_filter = await coroutined_pre_delete(document)

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

                await coroutined_post_delete(document, ret)

            return ret
