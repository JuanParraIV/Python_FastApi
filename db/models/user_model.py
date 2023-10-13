from pydantic import BaseModel
from typing import Optional

# Entidad User
class User(BaseModel):
    id: str | None
    username: str
    email: str
