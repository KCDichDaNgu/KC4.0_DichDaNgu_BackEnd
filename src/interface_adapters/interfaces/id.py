from abc import ABC
from pydantic import BaseModel
class Id(ABC, BaseModel):

    id: str
