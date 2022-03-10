from functools import partial
import re
from core.middlewares.authentication.auth_injection_interface import AuthInjectionInterface
from sanic.request import Request
from sanic import response
import aiohttp
from datetime import datetime, timedelta
from infrastructure.configs.message import MESSAGES

def init_auth(config, injection: AuthInjectionInterface):
    print(config)
    global AUTH_CONFIG
    global auth_injection

    AUTH_CONFIG = config
    auth_injection = injection

def login_required(async_handler=None, roles=['admin', 'member']):
    if async_handler is None:
        return partial(login_required, roles=roles)

    async def wrapped(route, request: Request, **kwargs):
        access_token = request.headers.get('Authorization')
        failed_response = response.json(
            status=403,
            body={
                'code': 0,
                'message': MESSAGES['unauthorized']
            }
        )
        
        if access_token is None:
            return failed_response

        token = await auth_injection.get_token(access_token)
        if token is None:
            return failed_response

        if token.props.revoked:
            return failed_response

        if datetime.now() > token.updated_at.value + timedelta(seconds=token.props.access_expires_in):
            return failed_response

        user = await auth_injection.get_user(token)

        if user.role not in roles:
            return failed_response

        return await async_handler(route, request, **kwargs)

    return wrapped

def active_required(async_handler=None, status=['active', 'inactive']):
    if async_handler is None:
        return partial(active_required, status=status)

    async def wrapped(route, request: Request, **kwargs):
        access_token = request.headers.get('Authorization')
        failed_response = response.json(
            status=403,
            body={
                'code': 0,
                'message': MESSAGES['inactive_user']
            }
        )
        
        if access_token is None:
            return failed_response

        token = await auth_injection.get_token(access_token)
        if token is None:
            return failed_response

        if token.props.revoked:
            return failed_response

        if datetime.now() > token.updated_at.value + timedelta(seconds=token.props.access_expires_in):
            return failed_response

        user = await auth_injection.get_user(token)

        if user.status not in status:
            return failed_response

        return await async_handler(route, request, **kwargs)

    return wrapped

async def create_token(user, platform):
    return await auth_injection.create_token(user, platform)

async def refresh_token(refresh_token):
    return await auth_injection.refresh_token(refresh_token)

async def revoke_token(request):
    access_token = request.headers.get('Authorization')
    
    if access_token is None:
        return None

    return await auth_injection.revoke_token(access_token)

async def get_me(request):
    access_token = request.headers.get('Authorization')
    
    if access_token is None:
        return None

    token = await auth_injection.get_token(access_token)

    if token is None:
        return None

    if token.props.revoked:
        return None

    if datetime.now() > token.updated_at.value + timedelta(seconds=token.props.access_expires_in):
        return None

    user = await auth_injection.get_user(token)
    if user is None:
        return None

    return user

async def get_user_from_provider(provider = "GOOGLE", **kwargs):
    providerAPI = getattr(AUTH_CONFIG, provider)
    async with aiohttp.ClientSession() as session:
        async with session.get(providerAPI.URL, params={**kwargs}) as response:
            result = await response.json()
            return result  
