from modules.user.commands.login.command import LoginCommand
from modules.user.commands.login.request_dto import LoginRequestDto
from modules.user.commands.create_user_by_admin.request_dto import CreateUserByAdminRequestDto
from infrastructure.configs.user import UserRole, UserStatus
from sanic.request import Request
from infrastructure.configs.message import MESSAGES

from sanic import response
from modules.user.commands.auth.request_dto import AuthUserRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.user.dtos.auth_user_response import AuthUserResponse

from core.middlewares.authentication.core import active_required, get_user_from_provider, create_token, refresh_token

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class Login(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        from modules.user.commands.auth.service import UserService
        self.__user_service = UserService()

    @doc.summary(APP_CONFIG.ROUTES['user.login']['summary'])
    @doc.description(APP_CONFIG.ROUTES['user.login']['desc'])
    @doc.consumes(LoginRequestDto, location="body", required=True)
    @doc.produces(AuthUserResponse)
    async def post(self, request: Request):
        try:
            data = request.json

            command = LoginCommand(
                username=data['username'],
                password=data['password'],
            )
            
            user = await self.__user_service.login(command)
            
            if (user.props.status == 'inactive'):
                return response.json(
                    status=501,
                    body={
                        'code': StatusCodeEnum.failed.value,
                        'message': MESSAGES['inactive_user']
                    }
                )
    
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
