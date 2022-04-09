from modules.system_setting.dtos.system_setting_response import SystemSettingResponse
from infrastructure.configs.message import MESSAGES
from interface_adapters.dtos.base_response import BaseResponse
from sanic_openapi import doc
from sanic.views import HTTPMethodView
from sanic import response
from infrastructure.configs.main import GlobalConfig, StatusCodeEnum, get_cnf

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class GetSystemSetting(HTTPMethodView):

    def __init__(self) -> None:

        from modules.system_setting.domain.service.system_setting_service import SystemSettingDService
        self.__system_setting_service = SystemSettingDService()

    @doc.summary(APP_CONFIG.ROUTES['system_setting.get']['summary'])
    @doc.description(APP_CONFIG.ROUTES['system_setting.get']['desc'])
    @doc.produces(SystemSettingResponse)
    
    async def get(self, request):
        saved_setting = await self.__system_setting_service.get()
        
        return response.json(BaseResponse(**{
            'code': StatusCodeEnum.success.value,
            'data': {
                'editorId': saved_setting.props.editor_id.value,
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
 