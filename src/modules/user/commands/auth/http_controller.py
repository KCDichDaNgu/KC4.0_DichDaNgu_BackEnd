from infrastructure.configs.user import UserRole, UserStatus
from modules.user.commands.auth.command import CreateUserCommand
from sanic.request import Request
from infrastructure.configs.message import MESSAGES

from sanic import response
from modules.user.commands.auth.request_dto import AuthUserRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView
from modules.user.dtos.auth_user_response import AuthUserResponse

from core.middlewares.authentication.core import get_user_from_provider, create_token, refresh_token

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class Auth(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        from modules.user.commands.auth.service import UserService
        self.__user_service = UserService()

    @doc.summary(APP_CONFIG.ROUTES['user.auth']['summary'])
    @doc.description(APP_CONFIG.ROUTES['user.auth']['desc'])
    @doc.consumes(AuthUserRequestDto, location="body", required=True)
    @doc.produces(AuthUserResponse)
    async def post(self, request: Request):
        try:
            data = request.json
            # create new user
            if 'access_token' in data:
                user = await get_user_from_provider(config.OAUTH2_PROVIDER.GOOGLE.NAME, access_token = data['access_token'])

                if 'error' in user:
                    return response.json(
                        status=404,
                        body={
                            'code': StatusCodeEnum.failed.value,
                            'message': MESSAGES['failed']
                        }
                    )
                command = CreateUserCommand(
                    username=user['email'],
                    first_name=user['given_name'],
                    last_name=user['family_name'],
                    email=user['email'],
                    password='',
                    avatar=user['picture'],
                    role=UserRole.member.value,
                    status=UserStatus.active.value,
                    text_translation_quota={
                        'vi-zh': 1000,
                        'vi-en': 1000,
                        'vi-km': 1000,
                        'vi-lo': 1000,
                    },
                )
                
                user = await self.__user_service.create_user(command)
                result = await create_token(user, data['platform'])

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

            # refresh access token
            if 'refresh_token' in data:
                result = await refresh_token(data['refresh_token'])
                if result:
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

            return response.json(
                status=400,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['failed']
                }
            )
        except Exception as error:
            print(error)
            return response.json(
                status=501,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['failed']
                }
            )
