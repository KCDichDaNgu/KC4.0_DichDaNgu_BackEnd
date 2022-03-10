from typing import List, get_args
from pydantic import Field
from core.base_classes.entity import BaseEntityProps
from pydantic.main import BaseModel
from core.base_classes import Entity
from core.value_objects import ID
from infrastructure.configs.token import Scope, TokenType, Platform

class TokenProps(BaseModel):

    user_id: ID = Field()
    token_type: TokenType = Field()
    access_token: ID = Field()
    refresh_token: ID = Field()
    scope: list = Field(...)
    platform: Platform = Field(...)
    access_expires_in: int = Field(...)
    refresh_expires_in: int = Field(...)
    revoked: bool = Field(...)

    class Config:
        use_enum_values = True

class TokenEntity(Entity[TokenProps]):

    def __init__(self, props: TokenProps) -> None:
        super().__init__(props)

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]
