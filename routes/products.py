from fastapi import APIRouter, HTTPException, status
from rich import print
import json

router = APIRouter(
    prefix="/instruments",
    tags=["Instruments"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

with open("./instruments.json", "r") as f:
    data = json.load(f)
instruments_list = data["instruments"]


def get_by_id(id: int):
    instruments = filter(lambda inst: inst.id == id, instruments_list)
    try:
        return instruments[0]
    except:
        return HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="Instrument no encontrado"
        )


@router.get("/")
async def all_instruments():
    if instruments_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No instruments found"
        )

    return instruments_list


@router.get("/{id}")
async def instruments(id: int):
    return get_by_id(id)
