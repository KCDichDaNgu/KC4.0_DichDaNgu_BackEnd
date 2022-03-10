from pydantic import BaseModel
from sanic.request import File

from core.value_objects.id import ID

class CreateFileLanguageDetectionRequestCommand(BaseModel):

    source_file: File
    
    class Config:
        arbitrary_types_allowed = True
