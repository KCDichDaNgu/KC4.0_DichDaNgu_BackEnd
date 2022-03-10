from pydantic import BaseModel

class LoginCommand(BaseModel):

    username: str
    password: str