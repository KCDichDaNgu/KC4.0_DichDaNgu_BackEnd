from pydantic.fields import PrivateAttr
from core.exceptions.base import ExceptionBase
from core.exceptions.type import ExceptionsEnum

class ArgumentNotProvidedException(ExceptionBase):

    __name: str = PrivateAttr(ExceptionsEnum.argument_not_provided.value)