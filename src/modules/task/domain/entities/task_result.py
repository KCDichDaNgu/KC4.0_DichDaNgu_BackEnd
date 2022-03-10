from time import time
from pydantic import Field
from pydantic.class_validators import root_validator, validator
from typing import Any, Optional, Union, get_args

from pydantic.fields import PrivateAttr
from core.base_classes.entity import Entity
from pydantic.main import BaseModel
from core.value_objects import ID

import aiofiles
import json, os

from infrastructure.configs.task import (
    TASK_RESULT_FILE_EXTENSION, get_task_result_file_name, get_task_result_file_path
)

from core.utils.file import get_full_path

class TaskResultProps(BaseModel):
    
    task_id: ID = Field(...)
    step: str = Field(...)
    file_path: Optional[str]

    @property
    def real_file_path(self):

        return get_full_path(get_task_result_file_path(self.file_path))

class TaskResultEntity(Entity[TaskResultProps]):
    
    @property
    def props_klass(self):
        return get_args(self.__orig_bases__[0])[0]

    async def save_request_result_to_file(self, content):

        if not self.props.file_path:
            
            self.props.file_path = get_task_result_file_name(
                created_at=int(round(time() * 1000)), 
                task_id=str(self.props.task_id.value),
                file_extension=TASK_RESULT_FILE_EXTENSION
            )

        full_file_path = self.props.real_file_path

        async with aiofiles.open(full_file_path, 'w+') as f:

            if isinstance(content, str):
                await f.write(json.dumps(json.loads(content)))
            else:
                await f.write(content)

            await f.close()

        return self.check_if_file_exists()

    async def read_data_from_file(self):

        full_file_path = self.props.real_file_path

        if not self.check_if_file_exists():

            raise FileNotFoundError('File not found')

        async with aiofiles.open(full_file_path) as f:
            
            data = await f.read()

            return json.loads(data)

    def check_if_file_exists(self):

        full_file_path = self.props.real_file_path
        
        return os.path.isfile(full_file_path)
