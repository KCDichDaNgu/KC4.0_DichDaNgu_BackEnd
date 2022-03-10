from infrastructure.configs.language import LanguageEnum
from interface_adapters.interfaces.translation_request.update_receiver_email import UpdateReceiverEmail
from sanic_openapi import doc

class UpdateReceiverEmailRequestDto(UpdateReceiverEmail):

    taskId: doc.String(
        description='taskId',
        required=True,
    )
    
    receiverEmail: doc.String(
        description='receiverEmail',
        required=True,
    )
    