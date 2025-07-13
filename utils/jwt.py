from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jsonwebtoken as jwt

from config import config

def encode_jwt(data: dict):
    return jwt.encode(data, config['TOKEN_KEY'], algorithm=config['TOKEN_ALGORITHM'])


def decode_jwt(token: str):
    return jwt.decode(token, config['TOKEN_KEY'], algorithms=[config['TOKEN_ALGORITHM']])


def check_jwt(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
    try:
        token = credentials.credentials
        return decode_jwt(token)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={ 'message': 'Unauthorized' },
        )
