
from sanic_openapi import doc
from sanic import response
from sanic.request import Request
from sanic.views import HTTPMethodView
from modules.user.commands.update_user_quota.command import UpdateUserQuotaCommand
from infrastructure.configs.message import MESSAGES
from infrastructure.configs.user import UserRole
from interface_adapters.dtos.base_response import BaseResponse
from modules.user.commands.update_user_quota.request_dto import UpdateUserQuotaDto

from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf
from core.middlewares.authentication.core import login_required

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class UpdateUserQuota(HTTPMethodView):

    def __init__(self) ->None:
        super().__init__()
        from modules.user.commands.auth.service import UserService
        from modules.user.commands.update_user_statistic.service import UpdateUserStatisticService
        self.__user_service = UserService()
        self.__update_user_statistic = UpdateUserStatisticService()

    @doc.summary(APP_CONFIG.ROUTES['admin.update_user_quota']['summary'])
    @doc.description(APP_CONFIG.ROUTES['admin.update_user_quota']['desc'])
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header')
    @doc.consumes(UpdateUserQuotaDto, location="body", required=True)
    @login_required(roles=[UserRole.admin.value])
    async def put(self, request: Request):
        try:
            data = request.json

            command = UpdateUserQuotaCommand(
                text_translation_quota=data['text_translation_quota'] if 'text_translation_quota' in data else None,
            )

            updated_user_quota = await self.__update_user_statistic.update_user_quota(data['id'], command)

            return response.json(BaseResponse(**{
                'code': StatusCodeEnum.success.value,
                'data': {
                    'textTranslationQuota': updated_user_quota.props.text_translation_quota,
                },
                'message': MESSAGES['success']
            }).dict())
            
        except Exception as error:
            print(error)
            return response.json(
                status=500,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['failed']
                }
            )