from infrastructure.configs.language import LanguageEnum
from sanic_openapi import doc

class CreateFileLanguageDetectionRequestDto():

    sourceText: doc.String(
        description='Source text',
        required=True,
    )
