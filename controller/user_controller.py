from typing import Annotated
from fastapi import APIRouter, Depends
from database.session import SessionDep
from service.user_service import UserService
from schema.user_schema import UserIn, UserUpdateIn
from view.user_view import UserOut
from security import login_dependency

router = APIRouter(prefix="/users", dependencies=[Depends(login_dependency)])
service = UserService()


@router.get("/read", response_model=list[UserOut])
def read_users(
        current_user: Annotated[dict[str, str, bool, bool], Depends(login_dependency)],
        session: SessionDep,
        limit: int,
        offset: int = 0):
    return service.read_users(current_user, session,  limit, offset)


@router.get("/read/{id}", response_model=UserOut)
def detail_user(
        current_user: Annotated[dict[str, str, bool, bool], Depends(login_dependency)],
        session: SessionDep,
        id: int):
    return service.detail_user(current_user, session,  id)


@router.post("/create", status_code=201)
def create_user(
        current_user: Annotated[dict[str, str, bool, bool], Depends(login_dependency)],
        session: SessionDep, body: UserIn
):
    return service.create_user(current_user, session, body)


@router.patch("/update/{id}", status_code=204)
def update_user(
        current_user: Annotated[dict[str, str, bool, bool], Depends(login_dependency)],
        session: SessionDep, id: int, body: UserUpdateIn):
    return service.update_user(current_user, session, id, body)


@router.delete("/delete/{id}", status_code=204)
def delete_user(
        current_user: Annotated[dict[str, str, bool, bool], Depends(login_dependency)],
        session: SessionDep, id: int):
    return service.delete_user(current_user, session, id)
