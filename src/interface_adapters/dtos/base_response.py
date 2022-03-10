from infrastructure.configs.message import MESSAGES
from typing import Any
from pydantic import BaseModel, Field
from pydantic.class_validators import root_validator
from infrastructure.configs import StatusCodeEnum

class BaseResponse(BaseModel):

    code: StatusCodeEnum = StatusCodeEnum.success.value
    data: Any
    message: str = Field(...)

    @root_validator(pre=True)
    def validate(cls, values):

        if not values['message'] in MESSAGES.values():
            raise ValueError('Message invalid')

        return values

