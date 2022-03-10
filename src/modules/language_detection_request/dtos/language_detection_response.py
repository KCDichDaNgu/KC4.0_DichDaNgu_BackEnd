from infrastructure.configs.task import LanguageDetectionTaskNameEnum
from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc

class DataStructure:

    taskId = doc.String(required=True)

    taskName = doc.String(
        required=True,
        choices=LanguageDetectionTaskNameEnum.enum_values()
    )

    languageDetectionHistoryId = doc.String(
        required=True
    )

class PlainTextLanguageDetectionRequestResponse(ResponseBase):
    
    data: DataStructure
class FileLanguageDetectionRequestResponse(ResponseBase):
    
    data: DataStructure
