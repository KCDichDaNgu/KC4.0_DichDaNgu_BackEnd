from infrastructure.database.base_classes.cassandra.orm_entity_base import OrmEntityBase
from typing import NewType, TypeVar
from core.value_objects.id import ID
from core.domain_events import DomainEvents
from infrastructure.adapters.logger import Logger
from core.ports.repository import FindManyPaginatedParams, RepositoryPort, DataWithPagination
from core.exceptions import NotFoundException
from infrastructure.database.base_classes.cassandra.orm_mapper_base import OrmMapperBase
from core.base_classes.entity import BaseEntityProps
from abc import ABC
from typing import Generic, List, TypeVar, Any, Union
from cassandra.cqlengine.query import BatchQuery

import asyncio

Entity = TypeVar('Entity', bound=BaseEntityProps)
EntityProps = TypeVar('EntityProps')
OrmEntity = TypeVar('OrmEntity', bound=OrmEntityBase)
OrmMapper = TypeVar('OrmMapper', bound=OrmMapperBase)

class OrmRepositoryBase(
    Generic[Entity, EntityProps, OrmEntity, OrmMapper], 
    RepositoryPort[Entity, EntityProps],
    ABC
):

    def __init__(
        self,
        repository: OrmEntityBase = None,
        mapper: OrmMapperBase = None,
        table_name: str = None
    ) -> None:

        self.__table_name__ = table_name
        
        self.__repository = repository

        self.__mapper: OrmMapperBase = mapper

        self.__logger: Logger = Logger(__name__)

        self.__relations: List[str] = []

    @property
    def mapper(self):
        return self.__mapper

    @property
    def logger(self):
        return self.__logger

    @property
    def repository(self):
        return self.__repository

    @property
    def table_name(self):
        return self.__table_name__

    @property
    def relations(self):
        return self.__relations
        
    async def create(self, entity: Entity, batch_ins: Any = None):
        
        orm_entity = self.__mapper.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)
        
        result = await self.__repository.async_create_with_trigger(
            **(orm_entity.to_dict()), 
            batch_ins=batch_ins
        )

        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.__mapper.to_domain_entity(result)

    async def update(self, entity: Entity, batch_ins: Any = None):

        orm_entity = self.__mapper.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)
        
        result = await self.__repository.async_update_with_trigger(
            **(orm_entity.to_dict()), 
            batch_ins=batch_ins
        )

        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.__mapper.to_domain_entity(result)

    async def find_one(
        self,
        **params: Any,
    ):

        found = await self.__repository.async_first(**params)

        return self.__mapper.to_domain_entity(found) if found else None

    async def find_one_or_throw(self, params: Any = {}):
        
        found = None

        try:
            found = await self.find_one(**params)
        
        except NotFoundException:
            print('Not found')

        return found
            

    async def find_one_by_id_or_throw(self, id: Union[ID, str]):

        try:
            found = await self.find_one(id=id)

        except NotFoundException:
            print('Not found')

        return found

    async def find_many(
        self, 
        params: Any, 
        skip: int = None, 
        limit: int = None,
        order_by: Any = None
    ):
        
        result = []
        
        if order_by is None:
            founds = await self.__repository.objects.filter(**params).async_all()
        else:
            founds = await self.__repository.objects.filter(**params).order_by(order_by).async_all()

        founds = founds[skip:limit]

        result = list(map(lambda found: self.__mapper.to_domain_entity(found), founds))

        return result  

    async def find_many_paginated(
        self,
        options: Any
    ):
        
        result = []

        founds = await self.__repository.async_filter(options.params)
        
        count = founds.count()

        founds = founds[options.pagination.skip : options.pagination.limit]
        founds = founds.order_by(options.order_by)

        for found in founds:
            result.append(self.__mapper.to_domain_entity(found))

        return DataWithPagination[type(result)](
            data=result,
            total_entries=count,
            per_page=options.pagination.limit,
            page=options.pagination.page
        )

    async def delete(self, entity: Entity, batch_ins: Any = None, batch_end=True, **extra_data) -> Entity:

        await DomainEvents.publish_events(entity.id, self.__logger)

        await self.__repository.filter(id=entity.id.value).async_delete_with_trigger()

        self.__logger.debug(f'[Entity deleted]: {type(entity).__name__} {entity.id}')

        return entity
        