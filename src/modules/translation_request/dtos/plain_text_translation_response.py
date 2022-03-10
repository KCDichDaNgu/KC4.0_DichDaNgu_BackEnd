from infrastructure.configs.task import TranslationTaskNameEnum
from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc

class DataStructure:

    taskId = doc.String(required=True)

    taskName = doc.String(
        required=True,
        choices=TranslationTaskNameEnum.enum_values()
    )

    translationHistoryId = doc.String(
        required=True
    )

class PlainTextTranslationRequestResponse(ResponseBase):
    
    data: DataStructure
