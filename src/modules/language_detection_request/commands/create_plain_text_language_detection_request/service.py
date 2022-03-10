from modules.language_detection_request.commands.create_plain_text_language_detection_request.command import CreatePlainTextLanguageDetectionRequestCommand
from modules.language_detection_request.domain.services.language_detection_request_service import LanguageDetectionRequestDService

class CreatePlainTextLanguageDetectionRequestService():

    def __init__(self) -> None:
        
        self.__language_detection_request_dservice = LanguageDetectionRequestDService()

    async def create_request(self, command: CreatePlainTextLanguageDetectionRequestCommand):

        return await self.__language_detection_request_dservice.create(command=command)
