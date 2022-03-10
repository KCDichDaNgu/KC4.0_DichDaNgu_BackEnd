from pydantic.fields import PrivateAttr
from core.exceptions.base import ExceptionBase
from core.exceptions.type import ExceptionsEnum

class NotFoundException(ExceptionBase):

    __name: str = PrivateAttr(ExceptionsEnum.not_found.value)
