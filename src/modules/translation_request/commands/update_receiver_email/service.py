from modules.translation_request.commands.update_receiver_email.command import UpdateReceiverEmailCommand
from modules.translation_request.domain.services.translation_request_service import TranslationRequestDService

class UpdateReceiverEmailService():

    def __init__(self) -> None:
        
        self.__translation_request_d_service = TranslationRequestDService()

    async def update_receiver_email(self, command: UpdateReceiverEmailCommand):

        return await self.__translation_request_d_service.update_receiver_email(command=command)
