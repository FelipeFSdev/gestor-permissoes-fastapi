import cryptocode
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database.session import SessionDep
from model.user_model import User
from schema.login_schema import LoginIn
from view.login_view import LoginOut
from security import decrypt_pass, get_token

router = APIRouter(prefix="/login")


@router.post("", response_model=LoginOut)
def get_auth(session: SessionDep, body: LoginIn):
    user_to_login = session.exec(select(User).where(
        User.cpf == body.cpf)).one_or_none()
    if not user_to_login:
        raise HTTPException(
            status_code=401, detail="Access denied. Verify your CPF or password."
        )
    clean_password = decrypt_pass(user_to_login.password)
    if clean_password != body.password:
        raise HTTPException(
            status_code=401, detail="Access denied. Verify your CPF or password.")

    name = user_to_login.name
    department = user_to_login.department
    is_manager = user_to_login.is_manager
    super_user = user_to_login.super_user
    token = get_token(name, department, is_manager, super_user)

    return {"name": name, "token": token}
