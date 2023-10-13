from rich import print
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


# Entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    city: str


users_list = [
    User(id=1, name="Juan", surname="Parra", age=30, city="Maracaibo"),
    User(id=2, name="Maria", surname="Guerra", age=30, city="Tachira"),
    User(id=3, name="Carla", surname="Parra", age=34, city="Maracaibo"),
]


@router.get("/usersjson")
async def usersjson():
    return [
        {"name": "Juan", "surname": "Parra", "age": "30", "city": "Maracaibo"},
        {"name": "Maria", "surname": "Guerra", "age": "30", "city": "Tachira"},
        {"name": "Carla", "surname": "Parra", "age": "34", "city": "Maracaibo"},
    ]


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Usuario no encontrado"
        )


def add_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe"
        )

    users_list.append(user)
    return user


@router.get("/users/")
async def users():
    return users_list


# Mediante Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Mediante Query
@router.get("/userquery/")
async def users(id: int):
    return search_user(id)


@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def post(user: User):
    return add_user(user)


@router.put("/user/")
async def put(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            return {"message": "Usuario Actualizado Correctamente", "data": user}
    if not found:
        return {"error": "No se ha actualizado el usuario"}


@router.delete("/user/{id}")
async def delete(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return {"message": "Usuario Eliminado Correctamente", "data": saved_user}
    if not found:
        return {"Error": "el Usuario no Existe"}
