from fastapi import HTTPException, Header
from typing import Annotated
from jose.jwt import decode
from config import JWT_SECRET


def check_authorization(Authorization: Annotated[str, Header()]):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Provide Authentication Header")
    try:
        jwt_token = Authorization.split(" ")[1]
        decoded = decode(jwt_token, JWT_SECRET, algorithms=["HS256"])
        return decoded["username"]
    except BaseException:
        raise HTTPException(status_code=400, detail="Invalid Authentication")
