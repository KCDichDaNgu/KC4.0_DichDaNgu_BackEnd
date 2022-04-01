from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.user import TRANSLATION_PAIR_VI_EN, TRANSLATION_PAIR_VI_ZH, TranslationPairEnum
from interface_adapters.dtos.base_response import BaseResponse
from infrastructure.configs.message import MESSAGES
from modules.translation_request.commands.create_plain_text_translation_request.command import CreatePlainTextTranslationRequestCommand
import re
from sanic import response
from modules.translation_request.commands.create_plain_text_translation_request.request_dto import CreatePlainTextTranslationRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from core.exceptions.argument_out_of_range import ArgumentOutOfRangeException

from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.translation_request.dtos.plain_text_translation_response import PlainTextTranslationRequestResponse
from core.middlewares.authentication.core import get_me
from core.value_objects.id import ID

from core.utils.text import count_chars

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class CreatePlainTextTranslationRequest(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()

        from modules.translation_request.commands.create_plain_text_translation_request.service import CreatePlainTextTranslationRequestService
        from modules.user.commands.update_user_statistic.service import UpdateUserStatisticService
        from modules.system_setting.database.repository import SystemSettingRepository

        self.__create_plain_text_translation_request_service = CreatePlainTextTranslationRequestService()
        self.__update_user_statistic = UpdateUserStatisticService()
        
        self.__system_setting_repo = SystemSettingRepository()
        
    async def is_allowed_total_chars(self, total_chars):
        
        system_setting = await self.__system_setting_repo.find_one({})
        
        allowed_total_chars_for_text_translation = system_setting.props.allowed_total_chars_for_text_translation
        
        if total_chars > allowed_total_chars_for_text_translation:
            return False
        
        return True


    @doc.summary(APP_CONFIG.ROUTES['translation_request.text_translation.create']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_request.text_translation.create']['desc'])
    @doc.consumes(CreatePlainTextTranslationRequestDto, location="body", required=True)
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header'
    )
    @doc.produces(PlainTextTranslationRequestResponse)

    async def post(self, request):

        user = await get_me(request)
        data = request.json 
        
        if not await self.is_allowed_total_chars(len(data['sourceText'])): 
            return ArgumentOutOfRangeException(
                message=MESSAGES['total_chars_exceeded_allowed'],
                metadata=dict(
                    code=StatusCodeEnum.failed.value,
                    data={}
                )
            )

        if request.headers.get('Authorization') and user:        
            translation_response = await self.create_private_plain_text_translation_request(data, user)
        else:
            translation_response = await self.create_public_plain_text_translation_request(data)

        return translation_response

    async def create_public_plain_text_translation_request(self, data):

        command = CreatePlainTextTranslationRequestCommand(
            creator_id=ID(None),
            source_text=data['sourceText'],
            source_lang=data['sourceLang'] if 'sourceLang' in data else None,
            target_lang=data['targetLang']
        )        

        new_task, new_translation_record = await self.__create_plain_text_translation_request_service.create_request(command)

        return response.json(BaseResponse(
            code=StatusCodeEnum.success.value,
            data={
                'taskId': new_task.id.value, 
                'taskName': new_task.props.task_name,
                'translationHitoryId': new_translation_record.id.value
            },
            message=MESSAGES['success']
        ).dict())

    async def create_private_plain_text_translation_request(self, data, user) -> response:

        if data['sourceLang'] == LanguageEnum.vi:
            pair = "{}-{}".format(data['sourceLang'], data['targetLang'])
        else:
            pair = "{}-{}".format(data['targetLang'], data['sourceLang'])

        if user is None:
            return response.json(
                status=401,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['unauthorized']
                }
            )

        character_count = count_chars(data['sourceText'])
            
        user_statistic_result =  await self.__update_user_statistic.update_text_translate_statistic(user.id, pair, character_count)

        if user_statistic_result['code'] == StatusCodeEnum.failed.value:
            return response.json(
                status=400,
                body=user_statistic_result
            )
        else:
            command = CreatePlainTextTranslationRequestCommand(
                creator_id=ID(user.id),
                source_text=data['sourceText'],
                source_lang=data['sourceLang'] if 'sourceLang' in data else None,
                target_lang=data['targetLang']
            )

            new_task, new_translation_record = await self.__create_plain_text_translation_request_service.create_request(command)

            return response.json(BaseResponse(
                code=StatusCodeEnum.success.value,
                data={
                    'taskId': new_task.id.value, 
                    'taskName': new_task.props.task_name,
                    'translationHitoryId': new_translation_record.id.value
                },
                message=MESSAGES['success']
            ).dict())