from typing import Optional
from pydantic import BaseModel

class UpdateOtherUserCommand(BaseModel):

    id: str
    role: str
    status: str
    text_translation_quota: Optional[dict]
