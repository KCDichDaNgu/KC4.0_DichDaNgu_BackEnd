from core.base_classes.entity import BaseEntityProps
from core.value_objects import DateVO, ID
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, get_args

from infrastructure.database.base_classes.mongodb import OrmEntityBase

Entity = TypeVar('Entity', bound=BaseEntityProps)
OrmEntity = TypeVar('OrmEntity')
Props = TypeVar('Props')

class OrmMapperBase(ABC, Generic[Entity, OrmEntity]):

    def __init__(self) -> None:
        super().__init__()

    @property
    @abstractmethod
    def entity_klass(self):
        # return get_args(self.__orig_bases__[0])[0]
        raise NotImplementedError()

    @property
    @abstractmethod
    def orm_entity_klass(self):
        # return get_args(self.__orig_bases__[0])[1]
        raise NotImplementedError()

    @abstractmethod
    def to_domain_props(self, orm_entity: OrmEntity) -> Any:
        return

    @abstractmethod
    def to_orm_props(self, entity: Entity) -> OrmEntity:
        return

    def to_domain_entity(self, orm_entity: OrmEntity) -> Entity:
        
        props = self.to_domain_props(orm_entity)
        
        return self.assign_props_to_entity(props, orm_entity)

    def to_orm_entity(self, entity: Entity) -> OrmEntity:

        props = self.to_orm_props(entity)
        
        return self.orm_entity_klass(**{
            **props,
            'id': entity.id.value,
            'created_at': entity.created_at.value,
            'updated_at': entity.updated_at.value
        })


    def assign_props_to_entity(
        self, 
        entity_props: Any,
        orm_entity: OrmEntity
    ) -> Entity:

        return self.entity_klass.from_orm({
            **entity_props,
            "id": ID(str(orm_entity.id)),
            "created_at": DateVO(orm_entity.created_at),
            "updated_at": DateVO(orm_entity.updated_at)
        })
