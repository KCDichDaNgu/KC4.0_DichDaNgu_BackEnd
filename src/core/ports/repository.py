from numbers import Complex
from pydantic.main import BaseModel
from core.base_classes.entity import BaseEntityProps
from core.value_objects.id import ID

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar, Awaitable, Any, Union, Dict

Entity = TypeVar('Entity')
EntityProps = TypeVar('EntityProps')
T = TypeVar('T')

order_by = Dict[str, Union[str, Complex]]

class Pagination(BaseModel):

    skip: Optional[int]
    limit: Optional[int]
    page: Optional[int]

class FindManyPaginatedParams(ABC, Generic[EntityProps]):

    params: Optional[Dict]
    pagination: Optional[Pagination]
    order_by: Optional[order_by]

class DataWithPagination(BaseModel):

    data: Any
    total_entries: int
    per_page: Optional[int]
    page: Optional[int]
    

class RepositoryPort(
    ABC, 
    Generic[Entity, EntityProps],
):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def create(self) -> Awaitable[Entity]:
        ...

    @abstractmethod
    def create_many(self) -> Awaitable[List[Entity]]:
        ...

    @abstractmethod
    def update(self) -> Awaitable[Entity]:
        ...

    @abstractmethod
    def update_many(self) -> Awaitable[List[Entity]]:
        ...

    @abstractmethod
    def find_one_or_throw(self) -> Awaitable[Entity]:
        ...

    @abstractmethod
    def delete(self):
        ...    
    
    @abstractmethod
    def delete_many(self):
        ...

    @abstractmethod
    def delete_many(self):
        ...

    @abstractmethod
    def find_many(self) -> Awaitable[List[Entity]]:
        ...

    @abstractmethod
    def find_many_paginated(
        self
    ) -> Awaitable[DataWithPagination]:
        ...
