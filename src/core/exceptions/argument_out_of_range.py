from pydantic.fields import PrivateAttr
from core.exceptions.base import ExceptionBase
from core.exceptions.type import ExceptionsEnum

class ArgumentOutOfRangeException(ExceptionBase):

    __name: str = PrivateAttr(ExceptionsEnum.argument_out_of_range.value)