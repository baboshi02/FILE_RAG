from fastapi import APIRouter
from models.user import User
from utils.jwt_wrapper import encode

router = APIRouter()
from payload_models.registeration import SigninPayload, LoginPayload


@router.post("/signin")
async def signin(payload: SigninPayload):
    email = payload.email
    password = payload.password
    username = payload.username
    await User.create(email=email, password=password, username=username)
    token = encode({"email": email, "username": username})
    return {"token": token}


@router.post("/login")
async def login(payload: LoginPayload):
    email = payload.email
    password = payload.password
    try:
        user = await User.get(email=email, password=password)
    except Exception:
        return {"message": "No user with given credentials"}
    token = encode({"email": user.email, "username": user.username})
    return {"token": token}
