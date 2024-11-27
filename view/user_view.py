from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    cpf: str
    password: str
    department: str
    is_manager: bool
    super_user: bool
