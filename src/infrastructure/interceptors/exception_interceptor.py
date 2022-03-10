from logging import exception
from core.exceptions import (
    ExceptionBase, 
    ConfictException,
    NotFoundException,
    DomainException,
    SanicConflictException
)

from sanic.handlers import ErrorHandler
from sanic.exceptions import Forbidden, NotFound

class ExceptionInterceptor(ErrorHandler):
    def default(self, request, exception: ExceptionBase):
        ''' handles errors that have no error handlers assigned '''
        
        if isinstance(exception, DomainException):
            raise Forbidden()
            
        if isinstance(exception, NotFoundException):
            raise NotFound()

        if isinstance(exception, ConfictException):
            raise SanicConflictException()

        return super().default(request, exception)
