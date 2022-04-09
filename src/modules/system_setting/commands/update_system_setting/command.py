from pydantic import BaseModel
from pydantic.types import conint
from typing import Optional

class UpdateSystemSettingCommand(BaseModel):

    task_expired_duration: float
    translation_api_url: Optional[str]
    translation_api_allowed_concurrent_req: int
    language_detection_api_url: Optional[str]
    language_detection_api_allowed_concurrent_req: int
    translation_speed_for_each_character: float
    language_detection_speed: float
    email_for_sending_email: str
    email_password_for_sending_email: str
    allowed_total_chars_for_text_translation: int
    allowed_file_size_in_mb_for_file_translation: float
