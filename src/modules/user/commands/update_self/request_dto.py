from interface_adapters.interfaces.user_request.update_user import UpdateUser
from sanic_openapi import doc

class UpdateUserRequestDto(UpdateUser):

    first_name: doc.String(
        description='First name of user to update',
        name='first_name'
    )

    last_name: doc.String(
        description='Last name of user to update',
        name='last_name',
    )

    avatar: doc.String(
        description='Avatar of user to update',
        name='avatar',
    )
