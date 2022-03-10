from pydantic import BaseModel
from typing import Union

from core.value_objects.id import ID

class CreatePlainTextTranslationRequestCommand(BaseModel):

    creator_id: Union[ID, None]
    source_text: str
    source_lang: Union[str, None]
    target_lang: str
