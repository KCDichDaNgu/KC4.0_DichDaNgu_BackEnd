from interface_adapters.base_classes.response import ResponseBase
from modules.user.commands.update_self.command import UpdateUserCommand
from sanic.request import Request
from infrastructure.configs.message import MESSAGES

from sanic import response
from modules.user.commands.update_self.request_dto import UpdateUserRequestDto
from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf

from sanic_openapi import doc
from sanic.views import HTTPMethodView

from core.middlewares.authentication.core import login_required, get_me

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class UpdateSelf(HTTPMethodView):

    def __init__(self) -> None:
        super().__init__()
        from modules.user.commands.update_self.service import UserService
        from modules.user.domain.services.user_service import UserDService
        self.__user_domain_service = UserDService()
        self.__user_service = UserService()

    @doc.summary(APP_CONFIG.ROUTES['user.update_self']['summary'])
    @doc.description(APP_CONFIG.ROUTES['user.update_self']['desc'])
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header')
    @doc.consumes(UpdateUserRequestDto, location="body", required=True)
    @doc.produces(ResponseBase)
    @login_required
    async def put(self, request: Request):
        try:
            data = request.json
            me = await get_me(request)

            if me is None:
                return response.json(
                    status=404,
                    body={
                        'code': StatusCodeEnum.failed.value,
                        'message': MESSAGES['failed']
                    }
                )
                
            user_statistic = await self.__user_domain_service.get_user_statistic(me.id)

            command = UpdateUserCommand(
                id=me.id,
                first_name=data['first_name'],
                last_name=data['last_name'],
                avatar=data['avatar'],
                text_translation_quota=user_statistic.props.text_translation_quota,
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
