from infrastructure.configs.language import LanguageEnum
from sanic_openapi import doc

class CreateFileTranslationRequestDto():
    
    sourceLang: doc.String(
        description='Source text language',
        required=False,
        choices=LanguageEnum.enum_values()
    )

    targetLang: doc.String(
        description='Translated text language',
        required=True,
        choices=LanguageEnum.enum_values()
    )
