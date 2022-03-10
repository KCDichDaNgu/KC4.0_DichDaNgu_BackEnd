from interface_adapters.interfaces.user_request.auth_user import AuthUser
from sanic_openapi import doc

class CreateUserByAdminRequestDto(AuthUser):

    username: doc.String(
        description='',
        name='username'
    )
    first_name: doc.String(
        description='',
        name='first_name'
    )
    last_name: doc.String(
        description='',
        name='last_name'
    )
    email: doc.String(
        description='',
        name='email'
    )
    password: doc.String(
        description='',
        name='password'
    )
    role: doc.String(
        description='',
        name='role'
    )
    status: doc.String(
        description='',
        name='status'
    )
    text_translation_quota: doc.Dictionary(
        description='',
        name='text_translation_quota',
    )
