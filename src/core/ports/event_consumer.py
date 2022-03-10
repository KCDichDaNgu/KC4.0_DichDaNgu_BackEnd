from abc import ABCMeta, abstractmethod
from logging import log

class EventConsumer(object, metaclass=ABCMeta):

    def __init__(self, log_service=None, service=None, listeners=None):
        super().__init__()

        self.__log_service = log_service

        self.__service = service
        self.__listeners = [] if listeners is None else []
        
        self.__assign_service_to_listeners()

    @property
    def log_service(self):
        return self.__log_service

    @log_service.setter
    def log_service(self, log_service):
        self.__log_service = log_service

    @property
    def service(self):
        return self.__service

    @service.setter
    def log_service(self, service):
        self.__assign_service_to_listeners()
        self.__service = service

    @property
    def listeners(self):
        self.__assign_service_to_listeners()
        return self.__listeners

    @listeners.setter
    def listeners(self, listeners):
        self.__assign_service_to_listeners()
        self.__listeners = listeners
        
    async def handle(self, message):
        for listener in self.__listeners:
            if listener.listens_to(message['name']):
                await listener.handle(message)


    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    def __assign_service_to_listeners(self):
        for listener in self.__listeners:
            listener.service = self.__service
