from fastapi import HTTPException, Header
from typing import Annotated
import dotenv
from jose.jwt import decode
import os

dotenv.load_dotenv
JWT_SECRET = os.getenv("JWT_SECRET") or ""


def check_authorization(Authorization: Annotated[str, Header()]):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Provide Authentication Header")
    try:
        jwt_token = Authorization.split(" ")[1]
        decode(jwt_token, JWT_SECRET, algorithms=["HS256"])
    except BaseException:
        raise HTTPException(status_code=400, detail="Invalid Authentication")
