from typing import get_args
from pydantic import Field

from core.value_objects.date import DateVO
from core.base_classes.entity import BaseEntityProps
from pydantic.main import BaseModel
from core.base_classes import Entity
from core.value_objects import ID
from infrastructure.configs.user import (
    UserStatus, UserRole
)

class UserProps(BaseModel):

    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    avatar: str = Field(...)
    role: UserRole = Field(...)
    status: UserStatus = Field(...)

    class Config: 
        use_enum_values = True

class UserEntity(Entity[UserProps]):

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    def validate_password(self, password):
        return password == self.props.password
