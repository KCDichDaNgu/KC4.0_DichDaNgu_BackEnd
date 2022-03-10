from pydantic import BaseModel

class CreatePlainTextLanguageDetectionRequestCommand(BaseModel):

    source_text: str
