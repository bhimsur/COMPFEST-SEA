from datetime import timedelta, datetime
import jwt

secret_key = '9c549d0f921253d4d7775087b5e304d36446e6b7a67407f1'
algorithm = 'HS256'


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_access_token(*, data: str):
    to_decode = data
    return jwt.decode(to_decode, secret_key, algorithm=algorithm)
