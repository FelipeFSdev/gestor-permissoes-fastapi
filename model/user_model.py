from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={
                           "autoincrement": True})
    name: str = Field(nullable=False)
    email: str = Field(nullable=False)
    cpf: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    department: str = Field(nullable=False)
    is_manager: bool = Field(default=False)
    super_user: bool = Field(default=False)
