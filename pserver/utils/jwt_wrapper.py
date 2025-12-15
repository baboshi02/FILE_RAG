from typing import Dict
from dotenv import load_dotenv
import jwt
import os

load_dotenv()


def encode(payload: Dict):
    jwt_secret = os.getenv("JWT_SECRET") or "secret"
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
