from pydantic import BaseModel
from infrastructure.configs.language import LanguageEnum

class CreatePlainTextTranslationRequest():

    sourceText: str
    sourceLang: str
    targetLang: str
