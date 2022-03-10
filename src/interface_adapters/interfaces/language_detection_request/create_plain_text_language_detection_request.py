from pydantic import BaseModel
from infrastructure.configs.language import LanguageEnum

class CreatePlainTextLanguageDetectionRequest():

    sourceText: str
