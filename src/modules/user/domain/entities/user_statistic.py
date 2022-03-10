from typing import List, get_args
from pydantic import Field
from pydantic.main import BaseModel
from core.base_classes import Entity
from core.value_objects import ID
from infrastructure.configs.main import StatusCodeEnum
from infrastructure.configs.message import MESSAGES
from interface_adapters.dtos.base_response import BaseResponse

class UserStatisticProps(BaseModel):

    user_id: ID = Field()
    text_translation_quota: dict = Field(...)
    total_translated_text: dict = Field(...)

    class Config:
        use_enum_values = True

class UserStatisticEntity(Entity[UserStatisticProps]):

    def __init__(self, props: UserStatisticProps) -> None:
        super().__init__(props)

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    def increase_total_translated_text(self, pair, text_length):

        pair_quota = self.props.text_translation_quota.get(pair, 1000)

        new_length = self.props.total_translated_text.get(pair, 0) + text_length

        if int(new_length) > int(pair_quota):

            return BaseResponse(**{
                "code": StatusCodeEnum.failed.value,
                "message": MESSAGES['text_translate_limit_reached'],
                "data": {
                    'used': self.props.total_translated_text.get(pair),
                    'quota': self.props.text_translation_quota.get(pair)
                }
            }).dict()            

        self.props.total_translated_text[pair] = new_length

        return BaseResponse(**{
            "code": StatusCodeEnum.success.value,
            "message": MESSAGES['success'],
            "data": self.props.total_translated_text
        }).dict()
