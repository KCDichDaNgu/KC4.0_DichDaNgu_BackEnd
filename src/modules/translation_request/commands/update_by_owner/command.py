from pydantic import BaseModel
from typing import Union, Optional

from core.value_objects.id import ID

class UpdateByOwnerCommand(BaseModel):

    id: Union[ID, None]
    rating: Optional[str]
    user_edited_translation: Optional[str]
