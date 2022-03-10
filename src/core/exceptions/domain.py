from pydantic.fields import PrivateAttr
from core.exceptions.base import ExceptionBase
from core.exceptions.type import ExceptionsEnum

class DomainException(ExceptionBase):

    __name: str = PrivateAttr(ExceptionsEnum.domain_exception.value)
