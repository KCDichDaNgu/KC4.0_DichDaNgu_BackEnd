from modules.language_detection_request.commands.create_file_language_detection_request.command import CreateFileLanguageDetectionRequestCommand
from modules.language_detection_request.domain.services.language_detection_request_service import LanguageDetectionRequestDService

class CreateFileLanguageDetectionRequestService():

    def __init__(self) -> None:
        
        self.__language_detection_request_dservice = LanguageDetectionRequestDService()

    async def create_request(self, command: CreateFileLanguageDetectionRequestCommand):
        return await self.__language_detection_request_dservice.create_file_detection_request(command=command)

