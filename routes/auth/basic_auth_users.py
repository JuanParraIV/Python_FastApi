from fastapi import APIRouter, Depends, HTTPException, status
from rich import print
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json


router = APIRouter(
    prefix="/basic_login",
    tags=["Basic"],
    responses={404: {"description": "Not found"}},
)

# Instancia de nuestro sistema Auth
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


# Base de datos de usuarios
users_db = {
    "juanp2": {
        "username": "juanp2",
        "password": "23893437",
        "email": "jmparra1993@gmail.com",
        "disabled": False,
        "rol": "user",
    },
    "DanielaUser": {
        "username": "DanielaUser",
        "email": "ledangom@gmail.com",
        "password": "1085325163*",
        "disabled": True,
        "rol": "user",
    },
}


# Entidad User
class User(BaseModel):
    username: str
    email: str
    disabled: bool
    rol: str


# Entidad UserDB
class UserDB(User):
    password: str


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de Autenticación invalida",
            headers={"WWW-Authenticate": "bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario Inactivo",
        )
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Obtener Usuario de la DB
    user_db = users_db.get(form.username)
    # Si no hay usuario
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
        )

    # Teniendo los datos del usuario verificar si la contraseña es correcta.

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="La contraseña no es correcta"
        )
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
