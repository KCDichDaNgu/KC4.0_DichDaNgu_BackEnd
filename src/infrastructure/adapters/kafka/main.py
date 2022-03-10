from infrastructure.interceptors.exeption_interceptor import ExceptionInterceptor
from infrastructure.adapters.kafka.kafka_event_producer import KafkaEventProducer
from infrastructure.adapters.kafka.kafka_event_consumer import KafkaEventConsumer
from core.ports.event_consumer import EventConsumer
from core.ports.event_producer import EventProducer
from infrastructure.configs.main import GlobalConfig


async def init_kafka(config: GlobalConfig):
    
    producer: EventProducer = KafkaEventProducer(
        bootstrap_servers=config.KAFKA_PRODUCER.BOOTSTRAP_SERVERS,
        topics=config.KAFKA_PRODUCER.TOPICS,
        log_service=None
    )

    await producer.start()
    
    consumer: EventConsumer = KafkaEventConsumer(
        bootstrap_servers=config.KAFKA_CONSUMER.BOOTSTRAP_SERVERS,
        topics=config.KAFKA_CONSUMER.TOPICS,
        log_service=None,
        group=config.KAFKA_CONSUMER.GROUP
    )

    await consumer.start()
