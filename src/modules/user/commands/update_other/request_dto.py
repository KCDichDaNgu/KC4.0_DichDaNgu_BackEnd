from interface_adapters.interfaces.user_request.update_other_user import UpdateOtherUser
from sanic_openapi import doc

class UpdateOtherUserRequestDto(UpdateOtherUser):

    id: doc.String(
        description='Id of user to update',
        name='id'
    )

    role: doc.String(
        description='Role of user to update',
        name='role'
    )

    status: doc.String(
        description='Status of user to update',
        name='status',
    )

    text_translation_quota: doc.Dictionary(
        description='Status of user to update',
        name='text_translation_quota',
    )
