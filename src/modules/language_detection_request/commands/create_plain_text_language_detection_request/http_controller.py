from interface_adapters.dtos.base_response import BaseResponse
from infrastructure.configs.message import MESSAGES
from modules.language_detection_request.commands.create_plain_text_language_detection_request.command import CreatePlainTextLanguageDetectionRequestCommand

from sanic import response
from modules.language_detection_request.commands.create_plain_text_language_detection_request.request_dto import CreatePlainTextLanguageDetectionRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.language_detection_request.dtos.language_detection_response import PlainTextLanguageDetectionRequestResponse

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class CreatePlainTextLanguageDetectionRequest(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        from modules.language_detection_request.commands.create_plain_text_language_detection_request.service import CreatePlainTextLanguageDetectionRequestService

        self.__create_plain_text_language_detection_request_service = CreatePlainTextLanguageDetectionRequestService()

    @doc.summary(APP_CONFIG.ROUTES['language_detection_request.text_language_detection.create']['summary'])
    @doc.description(APP_CONFIG.ROUTES['language_detection_request.text_language_detection.create']['desc'])
    @doc.consumes(CreatePlainTextLanguageDetectionRequestDto, location="body", required=True)
    @doc.produces(PlainTextLanguageDetectionRequestResponse)

    async def post(self, request):
        
        data = request.json

        command = CreatePlainTextLanguageDetectionRequestCommand(
            source_text=data['sourceText']
        )

        new_task, new_language_detection_record = await self.__create_plain_text_language_detection_request_service.create_request(command)

        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                'taskId': new_task.id.value,
                'taskName': new_task.props.task_name,
                'languageDetectionHistoryId': new_language_detection_record.id.value
            },
            'message': MESSAGES['success']
        }).dict())
