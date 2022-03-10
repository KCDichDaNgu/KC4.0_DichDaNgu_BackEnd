from pydantic import BaseModel, Field
from typing import List

class KafkaProducer(BaseModel):
    
    BOOTSTRAP_SERVERS: List[str] = None
    TOPICS: List[str] = None

class KafkaConsumer(BaseModel):

    BOOTSTRAP_SERVERS: List[str] = None
    TOPICS: List[str] = None
    GROUP: str = Field(None)
