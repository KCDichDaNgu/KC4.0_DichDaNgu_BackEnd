from numbers import Complex
from datetime import time, timedelta, date, datetime
from typing import Iterable, Union, List, Any

class Guard:

    @staticmethod
    def is_empty(value) -> bool:
        
        if value is None:
            return True

        if isinstance(value, Complex) or isinstance(value, bool):
            return False

        if isinstance(value, (time, timedelta, date, datetime)):
            return False

        if isinstance(value, dict) and not value:
            return True

        if isinstance(value, Iterable):
            if not value:
                return True
            
            if all([Guard.is_empty(e) for e in value]):
                return True
        
        if not value:
            return True

        return False
        
    @staticmethod
    def length_is_between(
        value: Union[Complex, str, List[Any]],
        min: Complex,
        max: Complex
    ) -> bool:

        if Guard.is_empty(value):
            raise Exception(
                'Cannot check length of a value. Provided value is empty'
            )

        value_length = len(str(Complex(value))) if isinstance(value, Complex) else len(value)

        if value_length >= min and value_length <= max:
            return True

        return False 
