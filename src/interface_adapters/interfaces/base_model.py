from abc import ABC
from pydantic import BaseModel

class ModelBase(ABC, BaseModel):

    id: str
    created_at: str
    updated_at: str 
