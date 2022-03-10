from interface_adapters.dtos.base_response import BaseResponse
from infrastructure.configs.message import MESSAGES
from modules.language_detection_request.commands.create_file_language_detection_request.command import CreateFileLanguageDetectionRequestCommand

from sanic import response
from modules.language_detection_request.commands.create_file_language_detection_request.request_dto import CreateFileLanguageDetectionRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf
from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.language_detection_request.dtos.language_detection_response import FileLanguageDetectionRequestResponse
from infrastructure.configs.translation_task import is_allowed_file_extension
from core.exceptions.argument_invalid import ArgumentInvalidException

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class CreateFileLanguageDetectionRequest(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        from modules.language_detection_request.commands.create_file_language_detection_request.service import CreateFileLanguageDetectionRequestService

        self.__create_file_language_detection_request_service = CreateFileLanguageDetectionRequestService()

    @doc.summary(APP_CONFIG.ROUTES['language_detection_request.doc_language_detection.create']['summary'])
    @doc.description(APP_CONFIG.ROUTES['language_detection_request.doc_language_detection.create']['desc'])
    @doc.consumes(
        doc.File(name="file"), 
        location="formData", 
        content_type="multipart/form-data",
    )
    @doc.produces(FileLanguageDetectionRequestResponse)

    async def post(self, request):
        
        file = request.files.get("file")

        if not is_allowed_file_extension(file.name):
            return ArgumentInvalidException(
                message=MESSAGES['failed'],
                metadata=dict(
                    code=StatusCodeEnum.failed.value,
                    data={}
                )
            )

        command = CreateFileLanguageDetectionRequestCommand(
            source_file=file
        )
        
        new_task, new_language_detection_record = await self.__create_file_language_detection_request_service.create_request(command)

        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                'taskId': new_task.id.value,
                'taskName': new_task.props.task_name,
                'languageDetectionHistoryId': new_language_detection_record.id.value
            },
            'message': MESSAGES['success']
        }).dict())
