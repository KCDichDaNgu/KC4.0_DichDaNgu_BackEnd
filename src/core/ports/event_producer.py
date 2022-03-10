from abc import ABC, abstractmethod

class EventProducer(ABC):

    def __init__(self, log_service=None):

        self.__log_service = log_service

    @property
    def log_service(self):
        return self.__log_service

    @log_service.setter
    def log_service(self, log_service):
        self.__log_service = log_service

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def flush(self, event):
        """
        Flush (actually publish) the events.
        """
        pass