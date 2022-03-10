from modules.user.commands.create_user_by_admin.request_dto import CreateUserByAdminRequestDto
from infrastructure.configs.user import UserRole, UserStatus
from modules.user.commands.create_user_by_admin.command import CreateUserCommand
from sanic.request import Request
from infrastructure.configs.message import MESSAGES

from sanic import response
from modules.user.commands.auth.request_dto import AuthUserRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.user.dtos.auth_user_response import AuthUserResponse

from core.middlewares.authentication.core import get_user_from_provider, create_token, login_required, refresh_token

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class CreateUserByAdmin(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        from modules.user.commands.auth.service import UserService
        self.__user_service = UserService()

    @doc.summary(APP_CONFIG.ROUTES['admin.create_user']['summary'])
    @doc.description(APP_CONFIG.ROUTES['admin.create_user']['desc'])
    @doc.consumes(CreateUserByAdminRequestDto, location="body", required=True)
    @login_required(roles=[UserRole.admin.value])
    async def post(self, request: Request):
        try:
            data = request.json

            command = CreateUserCommand(
                username=data['username'],
                first_name=data['first_name'] if 'first_name' in data else '',
                last_name=data['last_name'] if 'last_name' in data else '',
                email=data['email'],
                password=data['password'],
                role=data['role'],
                status=data['status'],
                text_translation_quota=data['text_translation_quota'],
            )
            
            user = await self.__user_service.create_user(command)

            result = await create_token(user, 'web')

            return response.json(body={
                'code': StatusCodeEnum.success.value,
                'data': {
                    'accessToken': result.props.access_token.value,
                    'refreshToken': result.props.refresh_token.value,
                    'tokenType': result.props.token_type,
                    'scope': result.props.scope
                },
                'message': MESSAGES['success']
            })

        except Exception as error:
            print(error)
            return response.json(
                status=501,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['failed']
                }
            )
