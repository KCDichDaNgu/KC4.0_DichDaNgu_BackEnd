from modules.translation_request.commands.update_by_owner.command import UpdateByOwnerCommand
from modules.translation_request.domain.services.translation_request_service import TranslationRequestDService

class UpdateByOwnerService():

    def __init__(self) -> None:
        
        self.__translation_request_d_service = TranslationRequestDService()

    async def update_by_owner(self, command: UpdateByOwnerCommand):

        return await self.__translation_request_d_service.update_by_owner(command=command)
