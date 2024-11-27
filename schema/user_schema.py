from pydantic import BaseModel


class UserIn(BaseModel):
    name: str
    email: str
    cpf: str
    password: str
    department: str
    is_manager: bool | None = False
    super_user: bool | None = False


class UserUpdateIn(BaseModel):
    name: str | None = None
    email: str | None = None
    cpf: str | None = None
    password: str | None = None
    department: str | None = None
    is_manager: bool | None = None
    super_user: bool | None = None
