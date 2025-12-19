from typing import Dict
import jwt
from config import JWT_SECRET


def encode(payload: Dict):
    jwt_secret = JWT_SECRET
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return token
