from typing import Any
from pydantic.fields import Field
from pydantic import BaseModel

from infrastructure.configs import StatusCodeEnum
from sanic_openapi import doc

class ResponseBase:

    code: doc.Integer(
        required=True,
        choices=StatusCodeEnum.enum_values()
    )

    data: Any

    message: doc.String(required=True)
