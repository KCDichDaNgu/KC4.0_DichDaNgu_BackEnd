from sanic.views import HTTPMethodView
from sanic_openapi.openapi2 import doc
from sanic import response
from core.utils.common import size_of

import io
from infrastructure.configs.user import TRANSLATION_PAIR_VI_EN, TRANSLATION_PAIR_VI_ZH, TranslationPairEnum
from core.utils.file import extract_file_extension, get_doc_file_meta, get_presentation_file_meta, get_txt_file_meta, get_worksheet_file_meta
from interface_adapters.dtos.base_response import BaseResponse
from infrastructure.configs.main import GlobalConfig, StatusCodeEnum, get_cnf

from modules.translation_request.commands.create_file_translation_request.command import CreateFileTranslationRequestCommand

from infrastructure.configs.message import MESSAGES
from infrastructure.configs.language import LanguageEnum
from infrastructure.configs.translation_task import is_allowed_file_extension

from core.exceptions.argument_invalid import ArgumentInvalidException
from core.exceptions.argument_out_of_range import ArgumentOutOfRangeException

from core.value_objects.id import ID
from core.middlewares.authentication.core import active_required, get_me


config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class CreateFileTranslationRequest(HTTPMethodView):
    def __init__(self) -> None:
        super().__init__()

        from modules.translation_request.commands.create_file_translation_request.service import CreateFileTranslationRequestService
        from modules.user.commands.update_user_statistic.service import UpdateUserStatisticService
        from modules.system_setting.database.repository import SystemSettingRepository
        
        self.__create_file_translation_request_service = CreateFileTranslationRequestService()
        self.__update_user_statistic = UpdateUserStatisticService()
        
        self.__system_setting_repo = SystemSettingRepository()
        
    async def is_allowed_file_size(self, file_size):
        
        system_setting = await self.__system_setting_repo.find_one({})
        
        allowed_file_size_in_mb_for_file_translation = system_setting.props.allowed_file_size_in_mb_for_file_translation
        
        if file_size > allowed_file_size_in_mb_for_file_translation:
            return False
        
        return True
        
    @doc.summary(APP_CONFIG.ROUTES['translation_request.doc_translation.create']['summary'])
    @doc.description(APP_CONFIG.ROUTES['translation_request.doc_translation.create']['desc'])
    @doc.consumes(
        doc.String(
            name="sourceLang",
            description='Source text language',
            required=False,
            choices=LanguageEnum.enum_values()
        ),
        location="formData"
    )
    @doc.consumes(
        doc.String(
            name="targetLang",
            description='Translated text language',
            required=True,
            choices=LanguageEnum.enum_values()
        ),
        location="formData"
    )
    @doc.consumes(
        doc.File(name="file"), 
        location="formData", 
        content_type="multipart/form-data",
    )
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header'
    )

    async def post(self, request):
        
        user = await get_me(request)
        file = request.files.get("file")
        data = request.form
        
        if not await self.is_allowed_file_size(size_of(file, 'mb')): 
            return ArgumentOutOfRangeException(
                message=MESSAGES['file_size_exceeded_allowed'],
                metadata=dict(
                    code=StatusCodeEnum.failed.value,
                    data={}
                )
            )

        if not is_allowed_file_extension(file.name):
            return ArgumentInvalidException(
                message=MESSAGES['failed'],
                metadata=dict(
                    code=StatusCodeEnum.failed.value,
                    data={}
                )
            )

        if request.headers.get('Authorization') and user:        
            translation_response = await self.create_private_file_translation_request(file, data, user)
        else:
            translation_response = await self.create_public_file_translation_request(file, data)

        return translation_response

    async def create_public_file_translation_request(self, file, data):

        command = CreateFileTranslationRequestCommand(
            creator_id=ID(None),
            source_file=file,
            source_lang=data['sourceLang'][0] if 'sourceLang' in data else None,
            target_lang=data['targetLang'][0]
        )        

        new_task, new_translation_record = await self.__create_file_translation_request_service.create_request(command)

        return response.json(BaseResponse(
            code=StatusCodeEnum.success.value,
            data={
                'taskId': new_task.id.value, 
                'taskName': new_task.props.task_name,
                'translationHitoryId': new_translation_record.id.value
            },
            message=MESSAGES['success']
        ).dict())

    async def create_private_file_translation_request(self, file, data, user) -> response:

        if data['sourceLang'] == LanguageEnum.vi:
            pair = "{}-{}".format(data['sourceLang'][0], data['targetLang'][0])
        else:
            pair = "{}-{}".format(data['targetLang'][0], data['sourceLang'][0])

        if user is None:
            return response.json(
                status=401,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['unauthorized']
                }
            )   

        file_ext = extract_file_extension(file.name)

        if file_ext == 'txt':
            character_count = get_txt_file_meta(file)
        elif file_ext == 'docx':
            character_count = get_doc_file_meta(file)[2]
        elif file_ext == 'pptx':
            character_count = get_presentation_file_meta(file)[3]
        elif file_ext == 'xlsx':
            character_count = get_worksheet_file_meta(file)[3]

        user_statistic_result =  await self.__update_user_statistic.update_text_translate_statistic(user.id, pair, character_count)

        if user_statistic_result['code'] == StatusCodeEnum.failed.value:
            return response.json(
                status=400,
                body=user_statistic_result
            )
        else:
            command = CreateFileTranslationRequestCommand(
                creator_id=ID(user.id),
                source_file=file,
                source_lang=data['sourceLang'][0] if 'sourceLang' in data else None,
                target_lang=data['targetLang'][0]
            )
            new_task, new_translation_record = await self.__create_file_translation_request_service.create_request(command)

            return response.json(BaseResponse(
                code=StatusCodeEnum.success.value,
                data={
                    'taskId': new_task.id.value, 
                    'taskName': new_task.props.task_name,
                    'translationHitoryId': new_translation_record.id.value
                },
                message=MESSAGES['success']
            ).dict())