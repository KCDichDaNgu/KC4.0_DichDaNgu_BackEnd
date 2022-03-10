from pydantic import BaseModel, PrivateAttr
from core.value_objects import DateVO, ID
from abc import ABC, abstractmethod

class DomainEvent(ABC, BaseModel):

    name: str = 'base'
    __date_occurred: DateVO = PrivateAttr()
    __aggregate_id: ID = PrivateAttr()

    def __init__(self, aggregate_id: ID) -> None:
        self.__date_occurred = DateVO.now()
        self.__aggregate_id = aggregate_id

    @property
    def aggregate_id(self) -> ID:
        raise self.__aggregate_id

    @property
    def date_occurred(self):
        return self.__date_occurred

    @abstractmethod
    def serialize(self):
        pass
