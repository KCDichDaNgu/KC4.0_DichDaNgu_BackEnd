from infrastructure.configs.language import LanguageEnum
from interface_adapters.interfaces.translation_request.update_receiver_email import UpdateReceiverEmail
from sanic_openapi import doc

class UpdateReceiverEmailRequestDto(UpdateReceiverEmail):

    taskId: doc.String(
        description='taskId',
        required=True,
    )
    
    rating: doc.String(
        description='rating',
        required=False,
    )
    
    userEditedTranslation: doc.String(
        description='userEditedTranslation',
        required=False,
    )
    