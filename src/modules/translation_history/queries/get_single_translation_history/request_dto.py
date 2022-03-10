from interface_adapters.interfaces.translation_request.get_single_translation_history import GetSingleTranslationHistory
from sanic_openapi import doc

class GetSingleTranslationHistoryRequestDto(GetSingleTranslationHistory):

    taskId: doc.String(
        description='Task Id',
        name='taskId'
    )

    translationHistoryId: doc.String(
        description='Translation History Id',
        required=False,
        name='translationHistoryId'
    )
    