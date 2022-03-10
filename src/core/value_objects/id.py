from typing import Any, Union
from pydantic import BaseModel
from core.utils.uuid import is_valid_uuid
from uuid import uuid4
from core.exceptions.argument_invalid import ArgumentInvalidException
from core.base_classes.value_object import (
    DomainPrimitive,
    ValueObject,
    ValueObjectProps
)
from core.utils import is_valid_uuid

class ID(ValueObject[str]):

    def __init__(self, value: Union[str, None], **data):

        super().__init__(ValueObjectProps[str](value), **data)

    @property
    def value(self) -> str:
        return self.props.value

    @staticmethod
    def generate():
        return ID(str(uuid4()))

    @classmethod
    def verify(cls, args: DomainPrimitive[str]):
        if not args.value is None and not is_valid_uuid(args.value):
            raise ArgumentInvalidException('Incorrect ID format') 