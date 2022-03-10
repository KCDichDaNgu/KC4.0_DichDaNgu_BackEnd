from typing import List, TypeVar

from pydantic.fields import PrivateAttr
from core.domain_events import DomainEvent, DomainEvents
from core.base_classes.entity import Entity

from abc import ABC

EntityProps = TypeVar('EntityProps')

class AggregateRoot(Entity[EntityProps]):

    __domain_events: List[DomainEvent] = PrivateAttr([])
    
    @property
    def domain_events(self) -> List[DomainEvent]:
        return self.__domain_events

    def add_event(self, domain_event: DomainEvent):

        self.__domain_events.append(domain_event)
        DomainEvents.prepare_for_publish(self)

    def create_events(self):

        self.__domain_events = []
