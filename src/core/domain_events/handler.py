from abc import ABC, abstractmethod

class DomainEventHandler(ABC):

    event_name = 'base'

    @abstractmethod
    def listens_to(self, event_name):
        pass

    @abstractmethod
    async def handle(self, message):
        pass

        