from pydantic import BaseModel


class LoginOut(BaseModel):
    name: str
    token: str
