
from sanic_openapi import doc

class UpdateUserQuotaDto():

    id: doc.String(
        description='Id of user to update',
        name='id'
    )

    text_translation_quota: doc.Dictionary(
        description='',
        name='text_translation_quota',
    )
