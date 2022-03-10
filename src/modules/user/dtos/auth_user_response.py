from interface_adapters.base_classes.response import ResponseBase
from sanic_openapi import doc

class DataStructure:

    access_token = doc.String(required=True)
    refresh_token = doc.String(required=True)
    token_type = doc.String(required=True)
    scope = doc.String(required=True)


class AuthUserResponse(ResponseBase):

    data: DataStructure
    