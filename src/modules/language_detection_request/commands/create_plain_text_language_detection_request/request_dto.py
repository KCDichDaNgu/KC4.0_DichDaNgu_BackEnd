from infrastructure.configs.language import LanguageEnum
from interface_adapters.interfaces.language_detection_request.create_plain_text_language_detection_request import CreatePlainTextLanguageDetectionRequest
from sanic_openapi import doc

class CreatePlainTextLanguageDetectionRequestDto(CreatePlainTextLanguageDetectionRequest):

    sourceText: doc.String(
        description='Source text',
        required=True,
    )
    