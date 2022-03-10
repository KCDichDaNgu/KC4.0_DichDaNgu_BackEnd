from interface_adapters.base_classes.response import ResponseBase
from infrastructure.configs.user import UserStatus, UserRole
from sanic_openapi import doc

class DataStructure:

    id = doc.String(required=True)
    username = doc.String(required=True)
    first_name = doc.String(required=True)
    last_name = doc.String(required=True)
    avatar = doc.String(required=True)
    email = doc.String(required=True)
    role = doc.String(required=True, choices=UserRole.enum_values())
    status = doc.String(required=True, choices=UserStatus.enum_values())
    created_at = doc.DateTime(required=True)
    updated_at = doc.DateTime(required=True)

class GetUserListResponse(ResponseBase):

    data: DataStructure