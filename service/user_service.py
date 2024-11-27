from fastapi import HTTPException
from sqlmodel import select, Session
from model.user_model import User
from schema.user_schema import UserIn, UserUpdateIn
from security import encrypt_pass


class UserService:
    def __check_cpf_length(self, cpf: int):
        if len(cpf) < 11 or len(cpf) > 11:
            raise HTTPException(
                status_code=400, detail="The cpf field must have 11 characters."
            )

    def __auth_charge(self, super_user: bool, manager: bool):
        if super_user is False and manager is False:
            raise HTTPException(
                status_code=403,
                detail="Access denied. You don't have sufficient permissions.",
            )

    def __auth_department(self, super_user: bool, department: str, body_dep: str):
        if body_dep:
            if super_user is False and department != body_dep.lower():
                raise HTTPException(
                    status_code=403,
                    detail="Access denied. You don't have sufficient permissions.",
                )

    def read_users(
        self,
        current_user: dict,
        session: Session,
        limit: int,
        offset: int,
    ):
        self.__auth_charge(
            current_user["super_user"], current_user["is_manager"])
        if current_user["super_user"] is True:
            users_list = session.exec(
                select(User).offset(offset).limit(limit)).all()
            if not users_list:
                raise HTTPException(status_code=404, detail="No users found.")

            return users_list
        users_list = session.exec(
            select(User)
            .where(User.department == current_user["department"])
            .offset(offset)
            .limit(limit)
        ).all()
        if not users_list:
            raise HTTPException(status_code=404, detail="No users found.")

        return users_list

    def detail_user(self, current_user: dict, session: Session, id: int):
        self.__auth_charge(
            current_user["super_user"], current_user["is_manager"])
        user_details = session.get(User, id)
        if not user_details:
            raise HTTPException(status_code=404, detail="User not found.")
        self.__auth_department(
            current_user["super_user"], current_user["department"], user_details.department
        )

        return user_details

    def create_user(self, current_user: dict, session: Session, body: UserIn):
        self.__auth_charge(
            current_user["super_user"], current_user["is_manager"])
        self.__auth_department(
            current_user["super_user"], current_user["department"], body.department
        )
        self.__check_cpf_length(body.cpf)
        check_duplicity = session.exec(
            select(User).where(User.cpf == body.cpf)
        ).one_or_none()
        if check_duplicity:
            raise HTTPException(
                status_code=400, detail="CPF's already registered in the system."
            )
        crypt_pass = encrypt_pass(body.password)
        new_user = User(
            name=body.name,
            email=body.email,
            cpf=body.cpf,
            password=crypt_pass,
            department=body.department.lower(),
            is_manager=body.is_manager,
            super_user=body.super_user,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {"message": "A new user has been created."}

    def update_user(
        self, current_user: dict, session: Session, id: int, body: UserUpdateIn
    ):
        self.__auth_charge(
            current_user["super_user"], current_user["is_manager"])
        self.__auth_department(
            current_user["super_user"], current_user["department"], body.department
        )
        if body.cpf:
            self.__check_cpf_length(body.cpf)
            check_duplicity = session.exec(
                select(User).where(User.cpf == body.cpf)
            ).one_or_none()
            if check_duplicity:
                raise HTTPException(
                    status_code=400, detail="CPF's already registered in the system."
                )

        user_to_update = session.get(User, id)
        if not user_to_update:
            raise HTTPException(status_code=404, detail="User not found.")
        self.__auth_department(
            current_user["super_user"], current_user["department"], user_to_update.department
        )

        data_to_update_user = body.model_dump(exclude_unset=True)
        user_to_update.sqlmodel_update(data_to_update_user)

        session.add(user_to_update)
        session.commit()
        session.refresh(user_to_update)
        return None

    def delete_user(self, current_user: dict, session: Session, id: int):
        self.__auth_charge(
            current_user["super_user"], current_user["is_manager"])
        user_to_delete = session.get(User, id)
        self.__auth_department(
            current_user["super_user"], current_user["department"], user_to_delete.department)
        if not user_to_delete:
            raise HTTPException(status_code=404, detail="User not found.")

        session.delete(user_to_delete)
        session.commit()
        return None
