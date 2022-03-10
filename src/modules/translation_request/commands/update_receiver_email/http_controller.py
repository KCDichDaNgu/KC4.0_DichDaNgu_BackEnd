import re
from infrastructure.configs.translation_task import TRANSLATION_PRIVATE_TASKS

from core.middlewares.authentication.core import get_me
from core.value_objects.id import ID

from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.main import GlobalConfig, StatusCodeEnum, get_cnf
from infrastructure.configs.message import MESSAGES
from infrastructure.configs.user import (TRANSLATION_PAIR_VI_EN,
                                         TRANSLATION_PAIR_VI_ZH,
                                         TranslationPairEnum)
from interface_adapters.dtos.base_response import BaseResponse

from modules.translation_request.commands.update_receiver_email.command import \
    UpdateReceiverEmailCommand
from modules.translation_request.commands.update_receiver_email.request_dto import \
    UpdateReceiverEmailRequestDto
from modules.translation_request.dtos.plain_text_translation_response import \
    PlainTextTranslationRequestResponse
    
from sanic import response
from sanic.views import HTTPMethodView
from sanic_openapi import doc

from uuid import UUID

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class UpdateReceiverEmail(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        
        from modules.translation_request.commands.update_receiver_email.service import \
            UpdateReceiverEmailService
        from modules.translation_request.database.translation_request.repository import TranslationRequestRepository

        self.__update_receiver_email_service = UpdateReceiverEmailService()
        self.__translation_request_repository = TranslationRequestRepository()

    @doc.summary(APP_CONFIG.ROUTES['translation_request.update_receiver_email']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_request.update_receiver_email']['desc'])
    @doc.consumes(UpdateReceiverEmailRequestDto, location="body", required=True)
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header'
    )
    @doc.produces(PlainTextTranslationRequestResponse)

    async def put(self, request):

        user = None
        
        if request.headers.get('Authorization'):
            user = await get_me(request)
        
        data = request.json 
        
        translation_request = await self.__translation_request_repository.find_one({'id': UUID(data['taskId'])})
        
        if not translation_request:
            return response.json(
                status=404,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['not_found']
                }
            )
            

        if translation_request.props.task_name in TRANSLATION_PRIVATE_TASKS and not user:
               
            return response.json(
                status=401,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['unauthorized']
                }
            ) 
            
        command = UpdateReceiverEmailCommand(
            id=ID(data['taskId']),
            receiver_email=data['receiverEmail']
        )  
            
        translation_request = await self.__update_receiver_email_service.update_receiver_email(command)

        return response.json(BaseResponse(
            code=StatusCodeEnum.success.value,
            data={},
            message=MESSAGES['success']
        ).dict())
