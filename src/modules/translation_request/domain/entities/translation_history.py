from pydantic import Field
from typing import Optional

from pydantic.fields import PrivateAttr
from core.base_classes.entity import Entity
from pydantic.main import BaseModel
from core.value_objects import ID

import aiofiles
import json, os

from infrastructure.configs.translation_history import TranslationHistoryTypeEnum, TranslationHistoryStatus

from typing import get_args

from core.utils.file import get_full_path
from infrastructure.configs.task import get_task_result_file_path

class TranslationHistoryProps(BaseModel):
    
    creator_id: ID
    task_id: ID = Field(...)
    translation_type: TranslationHistoryTypeEnum = Field(...)
    status: TranslationHistoryStatus = Field(...)
    file_path: Optional[str]

    class Config:
        use_enum_values = True

    @property
    def real_file_path(self):

        return get_full_path(get_task_result_file_path(self.file_path))
        
class TranslationHistoryEntity(Entity[TranslationHistoryProps]):

    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    async def save_result_file_path(self, file_path):

        self.props.file_path = file_path

    async def read_data_from_file(self):

        if not self.check_if_file_exists():

            raise FileNotFoundError('File not found')

        async with aiofiles.open(self.props.file_path) as f:
            
            data = json.load(f)

            f.close()

            return data

    async def check_if_file_exists(self):

        return os.path.isfile(self.props.file_path)
