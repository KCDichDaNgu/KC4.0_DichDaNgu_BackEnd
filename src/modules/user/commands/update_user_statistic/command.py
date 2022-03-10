from typing import Dict
from pydantic import BaseModel

class UpdateUserStatisticCommand(BaseModel):

    user_id: str
    total_translated_text: Dict
    text_translation_quota: Dict
