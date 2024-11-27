import jwt
import time
import cryptocode
from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from settings import ALGORITHM, SECRET_CRYPTO_PASS, SECRET_JWT_PASS


class JwtToken:
    exp: float
    name: str
    department: str
    is_manager: bool
    super_user: bool


def encrypt_pass(password: str):
    encrypted_password = cryptocode.encrypt(password, SECRET_CRYPTO_PASS)

    return encrypted_password


def decrypt_pass(encrypted_password: str):
    clean_password = cryptocode.decrypt(encrypted_password, SECRET_CRYPTO_PASS)
    if clean_password is False:
        raise HTTPException(
            status_code=401, detail="Access denied. Incorrect CPF or password."
        )

    return clean_password


def get_token(name: str, department: str, is_manager: bool, super_user: bool):
    payload = {
        "exp": time.time() + (30 * 60),
        "name": name,
        "department": department,
        "is_manager": is_manager,
        "super_user": super_user,
    }
    token = jwt.encode(payload, SECRET_JWT_PASS, ALGORITHM)

    return token


async def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_JWT_PASS, ALGORITHM)
        if decoded_token["exp"] >= time.time():
            return decoded_token
        else:
            return None
    except Exception:
        return None


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
):
    return await decode_token(token.credentials)


def login_dependency(
    current_user: Annotated[dict[str, str, bool, bool],
                            Depends(get_current_user)]
):
    if not current_user:
        raise HTTPException(
            status_code=401, detail="Invalid or expired token.")
    return current_user
