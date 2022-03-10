from datetime import datetime
from infrastructure.configs.main import GlobalConfig, get_cnf
from uuid import UUID
from infrastructure.database.base_classes.mongodb import OrmMapperBase, OrmEntityBase
from typing import Dict, TypeVar, List
from core.value_objects.id import ID
from core.domain_events import DomainEvents
from infrastructure.adapters.logger import Logger
from core.ports.repository import Pagination, RepositoryPort, DataWithPagination
from core.exceptions import NotFoundException
import pymongo
from core.base_classes.entity import BaseEntityProps
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar, Any

config: GlobalConfig = get_cnf()
PAGINATION_CONFIG = config.PAGINATION

Entity = TypeVar('Entity', bound=BaseEntityProps)
EntityProps = TypeVar('EntityProps')
OrmEntity = TypeVar('OrmEntity', bound=OrmEntityBase)
OrmMapper = TypeVar('OrmMapper', bound=OrmMapperBase)

class OrmRepositoryBase(
    Generic[Entity, EntityProps, OrmEntity, OrmMapper], 
    RepositoryPort[Entity, EntityProps],
    ABC
):
    
    def __init__(self) -> None:

        super().__init__()
            
        self.__logger: Logger = Logger(__name__)
        self.__mapper_ins = self.mapper()
    
    @property
    @abstractmethod
    def entity_klass(self):
        # return get_args(self.__orig_bases__[0])[0]
        raise NotImplementedError()

    @property
    @abstractmethod
    def repository(self):
        # return get_args(self.__orig_bases__[0])[1]
        raise NotImplementedError()

    @property
    @abstractmethod
    def mapper(self):
        # return get_args(self.__orig_bases__[0])[2]
        raise NotImplementedError()

    @property
    def logger(self):
        return self.__logger

    @property
    def mapper_ins(self):
        return self.__mapper_ins    
        
    async def create(self, entity: Entity):
        orm_entity = self.mapper_ins.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)
        
        await orm_entity.commit()

        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.mapper_ins.to_domain_entity(orm_entity)

    async def create_many(self, entities: List[Entity]):

        orm_entities = [self.mapper_ins.to_orm_entity(entity) for entity in entities]

        entities_ids = [entity.id for entity in entities]

        for id in entities_ids:

            await DomainEvents.publish_events(id, self.__logger)

        await self.insert_many(orm_entities)

        self.__logger.debug(f'[Entity persisted]: {type(entities[0]).__name__} {entities_ids}')

        return [self.mapper_ins.to_domain_entity(orm_entity) for orm_entity in orm_entities]


    async def update(self, entity: Entity, changes: Any, conditions: Dict = {}):
 
        orm_entity = self.mapper_ins.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)

        orm_entity.is_created = True
        
        changes['updated_at'] = datetime.now()
        orm_entity.update(changes)

        if conditions:
            await orm_entity.commit(conditions=conditions)
        else:
            await orm_entity.commit()
            
        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.mapper_ins.to_domain_entity(orm_entity)

    
    async def update_many(self, entities: List[Entity], changes: Any, conditions: Dict = {}):

        ...

    async def save(self, entity: Entity, update_conditions: Dict = {}):

        orm_entity = self.mapper_ins.to_orm_entity(entity)
        
        await DomainEvents.publish_events(entity.id, self.__logger)
        
        await orm_entity.commit(conditions=update_conditions)

        self.__logger.debug(f'[Entity persisted]: {type(entity).__name__} {entity.id}')
        
        return self.mapper_ins.to_domain_entity(orm_entity)

    async def find_one(
        self,
        params: Any,
    ):
    
        found = await self.repository.find_one(params)
        
        return self.mapper_ins.to_domain_entity(found) if found else None

    async def find_one_or_throw(self, params: Any = {}):
        
        found = None

        try:
            found = await self.find_one(params)
        
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
        
        cursor = self.repository.find(params)

        if skip:
            cursor = cursor.skip(skip)

        if limit:
            cursor = cursor.limit(limit)
        
        if order_by:
            cursor = cursor.sort(order_by)
            
        result = list((await cursor.to_list(length=None))) if not cursor is None else []
        
        result = list(map(lambda found: self.mapper_ins.to_domain_entity(found), result))

        return result  

    async def find_many_paginated(
        self,
        params: Any,
        pagination: Pagination,
        sort: Any,
    ):
        max_per_page = PAGINATION_CONFIG.MAX_PER_PAGE
        result = []

        founds = self.repository.find(params)
        total_entries = await self.repository.count_documents(params)
        
        if pagination['page']:
            founds = founds.skip((pagination['page'] - 1) * pagination['per_page'])

        if pagination['per_page']:
            founds = founds.limit(min(max_per_page, pagination['per_page']))

        if sort:
            founds = founds.sort(sort['key'], int(sort['direction']))

        result = list((await founds.to_list(length=None))) if not founds is None else []

        result = list(
            map(lambda found: self.mapper_ins.to_domain_entity(found), result))

        return DataWithPagination(
            data=result,
            total_entries=total_entries,
            per_page=pagination['per_page'],
            page=pagination['page']
        )

    async def delete(self, entity: Any) -> Entity:        

        await DomainEvents.publish_events(entity.id.value, self.__logger)

        query = {
            '_id': UUID(entity.id.value)
        }

        result = await self.repository.find_one(query)

        await result.delete()

        self.__logger.debug(f'[Entity deleted]: {entity.id.value}')

        return entity.id.value
        

    async def delete_many(self, entities: List[Any]):
        orm_entities = [self.mapper_ins.to_orm_entity(entity) for entity in entities]

        entities_ids = [entity.id for entity in entities]

        for id in entities_ids:

            await DomainEvents.publish_events(id, self.__logger)

        await self.repository.delete_many(orm_entities)

        self.__logger.debug(f'[Entity deleted]: {[UUID(entity.id.value) for entity in entities]}')

        return [UUID(entity.id.value) for entity in entities]

    async def delete_many_by_condition(self, conditions: Any):
        
        query = {}

        for condition in conditions:
            for key in condition:
                query[key] = {
                    '$in': [UUID(value) for value in condition[key]]
                }
    
        cursor = self.repository.find(query)

        result = list((await cursor.to_list(length=None)))

        await self.repository.delete_many(result)

        self.__logger.debug(f'[Entity deleted]: {[(entity.id) for entity in result]}')

        return [(entity.id) for entity in result]
