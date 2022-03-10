from pydantic.fields import PrivateAttr
from core.exceptions import ArgumentNotProvidedException
from core.guard import Guard
from core.utils import convert_props_to_object
from numbers import Complex
from typing import Any, Generic, Optional, TypeVar, Union, Final
from abc import ABC, abstractmethod
from pydantic import BaseModel

from datetime import datetime

Primitives = Union[str, Complex, bool]

T = TypeVar('T', Primitives, datetime)

class DomainPrimitive(Generic[T]):

    def __init__(self, value: T):
        self.value = value

class ValueObjectProps(Generic[T]):

    def __init__(self, value: Union[T, None]):

        if value == str(None): value = None

        self.value = value

class ValueObject(BaseModel, Generic[T]):

    __props: ValueObjectProps[T] = PrivateAttr(...)

    def __init__(self, props: ValueObjectProps[T], **data) -> None:

        super().__init__(**data)
        
        self.__props = props
        
        self.verify(props)

    @property
    def props(self):
        return self.__props

    @property
    def value(self):
        return self.__props.value

    @classmethod
    @abstractmethod
    def verify(cls, props: ValueObjectProps[T]):
        ...
    
    @staticmethod
    def is_value_object(obj):
        return isinstance(obj, ValueObject)

    def equals(self, vo: Optional[Any]) -> bool:
        if vo is None:
            return False
        
        return vo.props.value == self.props.value

    def get_raw_props(self) -> T:

        if self.is_domain_primitive(self.__props):
            return self.__props.value

        props_copy: Final = convert_props_to_object(self.__props)

        return props_copy

    def is_domain_primitive(self, obj: Any):

        if hasattr(obj, 'value') and isinstance(obj.value, Primitives.__args__):
            return True

        return False
        