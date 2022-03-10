from pydantic import BaseModel
from typing import Union

from core.value_objects.id import ID

class UpdateReceiverEmailCommand(BaseModel):

    id: Union[ID, None]
    receiver_email: str
