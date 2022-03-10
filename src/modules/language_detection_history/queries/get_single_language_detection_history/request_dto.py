from interface_adapters.interfaces.language_detection_request.get_single_language_detection_history import GetSingleLanguageDetectionHistory
from sanic_openapi import doc

class GetSingleLanguageDetectionHistoryRequestDto(GetSingleLanguageDetectionHistory):

    taskId: doc.String(
        description='Task Id',
        name='taskId'
    )

    languageDetectionHistoryId: doc.String(
        description='LanguageDetection History Id',
        required=False,
        name='languageDetectionHistoryId'
    )
    