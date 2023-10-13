### Users DB API ###
from fastapi import APIRouter, HTTPException, status
from rich import print
from pydantic import BaseModel
from db.dbclient import db_client
from db.models.user_model import User
from db.schemas.user_schema import user_schema, users_schema
from bson import ObjectId


router = APIRouter(
    prefix="/userdb",
    tags=["Users-DB"],
    responses={404: {"description": "Not found"}},
)

users_list = []


def search_user(field: str, key):
    try:
        user = db_client.test.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Usuario no encontrado"
        )


def add_user(user: User):
    if type(search_user("email",user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El E-Mail ya se encuentra registrado",
        )
    if type(search_user("username",user.username)) == User:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El nombre de usuario ya se encuentra registrado",
        )
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.test.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.test.users.find_one({"_id": id}))
    return User(**new_user)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def post(user: User):
    return add_user(user)


@router.get("/", response_model=list[User])
async def users():
    users = db_client.test.users.find()
    return users_schema(users)


# Mediante Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id",ObjectId(id))


# Mediante Query
@router.get("/")
async def users(id: str):
    return search_user("_id", ObjectId(id))


@router.put("/", response_model=User)
async def put(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.test.users.find_one_and_replace(
            {"_id":ObjectId(user.id)},
            user_dict,
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario No Encontrado",
        )
    return search_user("_id",ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str):
    found = db_client.test.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        return {"Error": "No se ha eliminado el usuario"}
    
    return {"msg":"Usuario eliminado correctamente"}
    
