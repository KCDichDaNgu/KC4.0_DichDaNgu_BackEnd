from infrastructure.configs.task import LanguageDetectionTaskNameEnum
from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc
from infrastructure.configs.language_detection_history import LanguageDetectionHistoryStatus

class DataStructure:

    taskId = doc.String(required=True)

    languageDetectionType = doc.String(
        required=True,
        choices=LanguageDetectionTaskNameEnum.enum_values()
    )

    status = doc.String(
        required=True,
        choices=LanguageDetectionHistoryStatus.enum_values()
    )

    resultUrl = doc.String(
        required=True
    )

    id = doc.String(
        required=True,
        choices=LanguageDetectionTaskNameEnum.enum_values()
    )

    updatedAt = doc.DateTime(
        required=True,
    )

    createdAt = doc.DateTime(
        required=True,
    )
    
    posInLangDetectionQueue = doc.Integer()
    estimatedWattingTime = doc.Float()

class SingleLanguageDetectionHistoryResponse(ResponseBase):
    
    data: DataStructure
