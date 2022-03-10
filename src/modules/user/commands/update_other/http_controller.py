from infrastructure.configs.user import UserRole
from interface_adapters.base_classes.response import ResponseBase
from modules.user.commands.update_other.command import UpdateOtherUserCommand
from sanic.request import Request
from infrastructure.configs.message import MESSAGES

from sanic import response
from modules.user.commands.update_other.request_dto import UpdateOtherUserRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView

from core.middlewares.authentication.core import login_required

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class UpdateOther(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        from modules.user.commands.update_other.service import UserService
        self.__user_service = UserService()

    @doc.summary(APP_CONFIG.ROUTES['user.update_other']['summary'])
    @doc.description(APP_CONFIG.ROUTES['user.update_other']['desc'])
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header')
    @doc.consumes(UpdateOtherUserRequestDto, location="body", required=True)
    @doc.produces(ResponseBase)
    @login_required(roles=[UserRole.admin.value])
    async def put(self, request: Request):
        try:
            data = request.json

            command = UpdateOtherUserCommand(
                id=data['id'],
                role=data['role'],
                status=data['status'],
                text_translation_quota=data['text_translation_quota'] if 'text_translation_quota' in data else None,
            )

            user = await self.__user_service.update_user(command)

            if user is None:
                return response.json(
                    status=400,
                    body={
                        'code': StatusCodeEnum.failed.value,
                        'message': MESSAGES['failed']
                    }
                )
            return response.json(body={
                'code': StatusCodeEnum.success.value,
                'message': MESSAGES['success']
            })

        except Exception as error:
            print(error)
            return response.json(
                status=500,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['failed']
                }
            )
