from core.ports import LoggerPort
from core.domain_events.base import DomainEvent
from typing import Any, Awaitable, Callable, Dict, List, TypeVar, Union, final
from core.value_objects.id import ID 
import asyncio

from asyncio import Task

from abc import ABC, abstractmethod 


class EventHandler(ABC):

    @abstractmethod
    def subscribeTo(event: DomainEvent):
        ...

EventCallback = Callable[[DomainEvent], Awaitable] 

EventName = str

DomainEventClass = DomainEvent

T = TypeVar('T', bound=DomainEvent)

@final
class DomainEvents():

    __subscribers: Dict[EventName, List[EventCallback]] = dict()
    __aggregates: List[Any] = []

    @classmethod
    def subscribe(
        cls,
        event: DomainEvent,
        callback: EventCallback
    ):
        event_name: EventName = event.name

        if not event_name in cls.__subscribers:

            cls.__subscribers.update({event_name: []})

        cls.__subscribers.get(event_name).append(callback)

    @classmethod
    def prepare_for_publish(
        cls,
        aggregate: Any
    ):

        aggregate_found = cls.find_aggregate_by_id(aggregate.id)

        if not aggregate_found:
            cls.__aggregates.append(aggregate)

    @classmethod
    async def publish_events(
        cls,
        id: ID,
        logger: LoggerPort
    ) -> Task:

        aggregate = cls.find_aggregate_by_id(id)

        if aggregate:

            domain_events = aggregate.domainEvents

            def publish_event(event: DomainEvent):
                logger.debug(
                    f'[Domain Event published]: {event.name} {aggregate.id.value}',
                )

                return domain_events.publish(event)

            await asyncio.wait(
                list(map(publish_event, domain_events)) + \
                [
                    aggregate.clear_events(),
                    cls.remove_aggregate_from_publish_list(aggregate)
                ]
            )

    @classmethod
    def find_aggregate_by_id(cls, id: ID) -> Union[Any, None]:
        
        for aggregate in cls.__aggregates:
            if aggregate.id.equals(id):
                return aggregate

    @classmethod
    def remove_aggregate_from_publish_list(
        cls,
        aggregate: Any
    ):

        cls.__aggregates = [e for e in cls.__aggregates if e.equals(aggregate)]

    @classmethod
    async def publish(cls, event: DomainEvent):
        event_name: str = event.name

        if event_name in cls.__subscribers:

            callbacks: List[EventCallback] = cls.__subscribers.get(event_name) or []
            
            await asyncio.wait(
                list(map(lambda callback: callback(event), callbacks))
            )

