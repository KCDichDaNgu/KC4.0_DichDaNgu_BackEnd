from interface_adapters.interfaces.user_request.auth_user import AuthUser
from sanic_openapi import doc

class AuthUserRequestDto(AuthUser):

    access_token: doc.String(
        description='Access token user get from Google',
        name='access_token'
    )

    platform: doc.String(
        description='Platform which user accesses from. Must be web/ios/android',
        name='platform'
    )

    refresh_token: doc.String(
        description='Token for getting new access_token of translate system. Note: Ignored when access_token is provided',
        name='refresh_token',
    )
    