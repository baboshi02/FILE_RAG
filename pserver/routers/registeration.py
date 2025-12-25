from fastapi import APIRouter
from models.user import User
from utils.jwt_wrapper import encode
from tortoise.exceptions import MultipleObjectsReturned, DoesNotExist

router = APIRouter()
from payload_models.registeration import SigninPayload, LoginPayload

# TODO : Test endpoints


@router.post("/signin")
async def signin(payload: SigninPayload):
    email = payload.email
    password = payload.password
    username = payload.username
    try:
        await User.create(email=email, password=password, username=username)
        user = await User.get(email=email, username=username).values("id")
    except MultipleObjectsReturned or DoesNotExist:
        return {"message": "Error while querying user"}
    token = encode({"id": user["id"]})
    return {"token": token}


@router.post("/login")
async def login(payload: LoginPayload):
    email = payload.email
    password = payload.password
    try:
        user = await User.get(email=email, password=password).values("id")
    except Exception:
        return {"message": "No user with given credentials"}
    token = encode({"id": user["id"]})
    return {"token": token}
