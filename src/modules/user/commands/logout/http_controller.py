from sanic_openapi import doc
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic import response

from infrastructure.configs.main import StatusCodeEnum, GlobalConfig, get_cnf
from infrastructure.configs.message import MESSAGES

from core.middlewares.authentication.core import revoke_token

config: GlobalConfig = get_cnf()
APP_CONFIG = config.APP_CONFIG

class Logout(HTTPMethodView):

    @doc.summary(APP_CONFIG.ROUTES['user.logout']['summary'])
    @doc.description(APP_CONFIG.ROUTES['user.logout']['desc'])
    @doc.consumes(
        doc.String(
            description="Access token",
            name='Authorization'
        ),
        location='header')
    async def post(self, request: Request):
        result = await revoke_token(request)
        if result is None:
            return response.json(
                status=400,
                body={
                    'code': StatusCodeEnum.failed.value,
                    'message': MESSAGES['failed']
                }
            )
        return response.json(
            body={
                'code': StatusCodeEnum.success.value,
                'message': MESSAGES['success']
            }
        )
