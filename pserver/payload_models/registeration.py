from pydantic import BaseModel


class SigninPayload(BaseModel):
    email: str
    password: str
    username: str


class LoginPayload(BaseModel):
    email: str
    password: str
