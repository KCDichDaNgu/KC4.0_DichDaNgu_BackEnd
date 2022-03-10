from core.base_classes.entity import BaseEntityProps
from core.value_objects import DateVO, ID
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from infrastructure.database.base_classes.cassandra.orm_entity_base import OrmEntityBase

Entity = TypeVar('Entity', bound=BaseEntityProps)
OrmEntity = TypeVar('OrmEntity')
Props = TypeVar('Props')

class OrmMapperBase(ABC, Generic[Entity, OrmEntity]):

    def __init__(self, entity_klass=None) -> None:
        super().__init__()

        self.__entity_klass = entity_klass

    @abstractmethod
    def to_domain_props(self, orm_entity: OrmEntity) -> Any:
        return

    @abstractmethod
    def to_orm_entity(self, entity: Entity) -> OrmEntity:
        return

    def to_domain_entity(self, orm_entity: OrmEntity) -> Entity:
        
        props = self.to_domain_props(orm_entity)
        
        return self.assign_props_to_entity(props, orm_entity)

    def to_orm_entity(self, entity: Entity) -> OrmEntity:

        props = self.to_orm_entity(entity)

        return OrmEntityBase(**{
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

        return self.__entity_klass.from_orm({
            **entity_props,
            "id": ID(str(orm_entity.id)),
            "created_at": DateVO(orm_entity.created_at),
            "updated_at": DateVO(orm_entity.updated_at)
        })
