from pydantic.class_validators import root_validator, validator
from typing import Union, Optional
from pydantic import Field, BaseModel 

from addict import Addict

from core.base_classes.entity import Entity
from core.value_objects import DateVO, ID

from typing import get_args

class SystemSettingProps(BaseModel):

    editor_id: ID = Field(...)
    task_expired_duration: int = Field(...)
    
    translation_api_url: Optional[str]
    translation_api_allowed_concurrent_req: int = Field(...)
    language_detection_api_url: Optional[str]
    language_detection_api_allowed_concurrent_req: int = Field(...)
    translation_speed_for_each_character: float = Field(...)
    language_detection_speed: float = Field(...)
    email_for_sending_email: str = Field(...)
    email_password_for_sending_email: str = Field(...)
    allowed_total_chars_for_text_translation: int = Field(...)
    allowed_file_size_in_mb_for_file_translation: float = Field(...)

    class Config:
        use_enum_values = True

    @root_validator(pre=True)
    def validate(cls, values):
        return values

class SystemSettingEntity(Entity[SystemSettingProps]):
    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]
