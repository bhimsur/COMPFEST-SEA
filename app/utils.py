import jwt
import time

secret_key = '9c549d0f921253d4d7775087b5e304d36446e6b7a67407f1'
algorithm = 'HS256'


def create_access_token(data: dict):
    payload = {
        'data': data,
        'expires': time.time()+600
    }
    encoded_jwt = jwt.encode(payload, secret_key, algorithm='HS256')
    return encoded_jwt


def decode_access_token(data: str):
    return jwt.decode(data, secret_key, algorithms=[algorithm])
