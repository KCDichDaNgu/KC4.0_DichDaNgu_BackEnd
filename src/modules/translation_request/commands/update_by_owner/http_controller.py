import re
from infrastructure.configs.translation_task import TRANSLATION_PRIVATE_TASKS,TRANSLATION_PUBLIC_TASKS

from core.middlewares.authentication.core import get_me
from core.value_objects.id import ID

from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.main import GlobalConfig, StatusCodeEnum, get_cnf
from infrastructure.configs.message import MESSAGES
from infrastructure.configs.user import (TRANSLATION_PAIR_VI_EN,
                                         TRANSLATION_PAIR_VI_ZH,
                                         TranslationPairEnum)
from interface_adapters.dtos.base_response import BaseResponse

from modules.translation_request.commands.update_by_owner.command import \
    UpdateByOwnerCommand
from modules.translation_request.commands.update_by_owner.request_dto import \
    UpdateReceiverEmailRequestDto
from modules.translation_request.dtos.plain_text_translation_response import \
    PlainTextTranslationRequestResponse
    
from sanic import response
from sanic.views import HTTPMethodView
from sanic_openapi import doc

from uuid import UUID

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class UpdateByOwner(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        
        from modules.translation_request.commands.update_by_owner.service import UpdateByOwnerService
        from modules.translation_request.database.translation_request.repository import TranslationRequestRepository
        from modules.translation_request.database.translation_history.repository import TranslationHistoryRepository

        self.__update_by_owner_service = UpdateByOwnerService()
        self.__translation_history_repository = TranslationHistoryRepository()

    @doc.summary(APP_CONFIG.ROUTES['translation_request.update_by_owner']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_request.update_by_owner']['desc'])
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
        
        translation_history = await self.__translation_history_repository.find_one({'id': UUID(data['id'])})
        
        if not translation_history:
            return response.json(
                status=404,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['not_found']
                }
            )
            
        if (translation_history.props.translation_type in TRANSLATION_PRIVATE_TASKS and not user) or \
            (user and translation_history.props.translation_type in TRANSLATION_PRIVATE_TASKS and translation_history.props.creator_id.value != user.id):
               
            return response.json(
                status=401,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['unauthorized']
                }
            ) 
            
        changes = dict(id=ID(data['id']))
            
        if 'rating' in data:
            changes.update(
                rating=data.get('rating', None),
            )
            
        if 'userEditedTranslation' in data:
            changes.update(
                user_edited_translation=data.get('userEditedTranslation', None),
            )
            
        command = UpdateByOwnerCommand(
            **changes
        )  
            
        translation_history = await self.__update_by_owner_service.update_by_owner(command)
        
        return response.json(BaseResponse(
            code=StatusCodeEnum.success.value,
            data={
                'taskId': translation_history.props.task_id.value,
                'translationType': translation_history.props.translation_type,
                'id': translation_history.id.value,
                'status': translation_history.props.status,
                'updatedAt': str(translation_history.updated_at.value),
                'createdAt': str(translation_history.created_at.value),
                'resultUrl': translation_history.props.real_file_path,
                'rating': translation_history.props.rating,
                'userEditedTranslation': translation_history.props.user_edited_translation,
            },
            message=MESSAGES['success']
        ).dict())
