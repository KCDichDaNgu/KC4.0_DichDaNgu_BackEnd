from pydantic import BaseModel

class CreateUserCommand(BaseModel):

    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    avatar: str
    role: str
    status: str
    text_translation_quota: dict
