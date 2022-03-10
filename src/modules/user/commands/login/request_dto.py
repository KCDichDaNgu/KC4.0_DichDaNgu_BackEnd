from interface_adapters.interfaces.user_request.auth_user import AuthUser
from sanic_openapi import doc

class LoginRequestDto(AuthUser):

    username: doc.String(
        description='',
        name='username'
    )

    password: doc.String(
        description='',
        name='password'
    )