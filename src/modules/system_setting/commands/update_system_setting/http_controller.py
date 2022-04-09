from modules.system_setting.dtos.system_setting_response import SystemSettingResponse
from sanic import response
from modules.system_setting.commands.update_system_setting.command import UpdateSystemSettingCommand
from modules.system_setting.commands.update_system_setting.request_dto import UpdateSystemSettingDto
from infrastructure.configs.message import MESSAGES
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf
from interface_adapters.dtos.base_response import BaseResponse

from infrastructure.configs.user import UserRole

from core.middlewares.authentication.core import login_required

from sanic_openapi import doc
from sanic.views import HTTPMethodView

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class Body:
    data = doc.Object(UpdateSystemSettingDto)

class UpdateSystemSetting(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        
        from modules.system_setting.domain.service.system_setting_service import SystemSettingDService

        self.__system_setting_service = SystemSettingDService()

    @doc.summary(APP_CONFIG.ROUTES['system_setting.update']['summary'])
    @doc.description(APP_CONFIG.ROUTES['system_setting.update']['desc'])
    @doc.consumes(Body, location="body")
    @doc.produces(SystemSettingResponse)
    @login_required(roles=[UserRole.admin.value])
    async def put(self, request):

        data = request.json['data']

        command = UpdateSystemSettingCommand(
            task_expired_duration=float(data['taskExpiredDuration']),
            # translation_api_url=data['translationApiUrl'],
            translation_api_allowed_concurrent_req=data['translationApiAllowedConcurrentReq'],
            # language_detection_api_url=data['languageDetectionApiUrl'],
            language_detection_api_allowed_concurrent_req=data['languageDetectionApiAllowedConcurrentReq'],
            translation_speed_for_each_character=float(data['translationSpeedForEachCharacter']),
            language_detection_speed=float(data['languageDetectionSpeed']),
            email_for_sending_email=data['emailForSendingEmail'],
            email_password_for_sending_email=data['emailPasswordForSendingEmail'],
            allowed_total_chars_for_text_translation=data['allowedTotalCharsForTextTranslation'],
            allowed_file_size_in_mb_for_file_translation=data['allowedFileSizeInMbForFileTranslation'],
        )

        saved_setting = await self.__system_setting_service.update(command)

        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                'taskExpiredDuration': saved_setting.props.task_expired_duration,
                'translationApiUrl': saved_setting.props.translation_api_url,
                'translationApiAllowedConcurrentReq': saved_setting.props.translation_api_allowed_concurrent_req,
                'languageDetectionApiUrl': saved_setting.props.language_detection_api_url,
                'languageDetectionApiAllowedConcurrentReq': saved_setting.props.language_detection_api_allowed_concurrent_req,
                'translationSpeedForEachCharacter': saved_setting.props.translation_speed_for_each_character,
                'languageDetectionSpeed': saved_setting.props.language_detection_speed,
                'emailForSendingEmail': saved_setting.props.email_for_sending_email,
                'emailPasswordForSendingEmail': saved_setting.props.email_password_for_sending_email,
                'allowedTotalCharsForTextTranslation': saved_setting.props.allowed_total_chars_for_text_translation,
                'allowedFileSizeInMbForFileTranslation': saved_setting.props.allowed_file_size_in_mb_for_file_translation,
            },
            'message': MESSAGES['success']
        }).dict())
 