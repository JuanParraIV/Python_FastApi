from fastapi import APIRouter, Depends, HTTPException, status
from rich import print
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1

router = APIRouter(
    prefix="/auth",
    tags=["JWT"],
    responses={404: {"description": "Not found"}},
)

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

bcrypt = CryptContext(
    schemes=["bcrypt"],
)


# Entidad User
class User(BaseModel):
    username: str
    email: str
    disabled: bool
    rol: str


# Entidad UserDB
class UserDB(User):
    password: str


# Base de datos de usuarios
users_db = {
    "juanp2": {
        "username": "juanp2",
        "password": "$2a$12$jVH1zLnR8JGP.3fxlZtEy.YuQiKYjRYfxVXPygg69DaGvsn2OtiLS",
        "email": "jmparra1993@gmail.com",
        "disabled": False,
        "role": "user",
    },
    "DanielaUser": {
        "username": "DanielaUser",
        "email": "ledangom@gmail.com",
        "password": "$2a$12$uBDGKeOlFQY5II.ZgUQ.3upBVKI/zzHPtsZZnk5hti3hM6Jivjvdy",
        "disabled": False,
        "role": "user",
    },
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciales de Autenticación invalida",
    headers={"WWW-Authenticate": "bearer"},
)


async def auth_user(token: str = Depends(oauth2)):
    try:
        username = jwt.decode(token, key="123", algorithms=ALGORITHM).get("sub")
        if username is None:
            raise EXCEPTION
    except JWTError:
        raise EXCEPTION

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
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

    compare_password = bcrypt.verify(form.password, user.password)

    if not compare_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta",
        )
    ACCESS_TOKEN_EXPIRATION = timedelta(minutes=ACCESS_TOKEN_DURATION)

    expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRATION

    # Generar el token JWT
    access_token = jwt.encode(
        {"sub": user.username, "exp": expire}, key="123", algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
