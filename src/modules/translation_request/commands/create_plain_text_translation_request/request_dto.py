from infrastructure.configs.language import LanguageEnum
from interface_adapters.interfaces.translation_request.create_plain_text_translation_request import CreatePlainTextTranslationRequest
from sanic_openapi import doc

class CreatePlainTextTranslationRequestDto(CreatePlainTextTranslationRequest):

    sourceText: doc.String(
        description='Source text',
        required=True,
    )

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
    