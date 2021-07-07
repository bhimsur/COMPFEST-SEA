from typing import List
import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPBasicCredentials
from datetime import timedelta
from starlette.responses import RedirectResponse
from jwt import PyJWTError

# from .schemas import UserBase, UserInfo
# from .models import Base, UserTable
# from .database import engine, SessionLocal
# from .crud import get_user

from app import schemas, models, database, crud
from app.utils import decode_access_token, create_access_token

models.Base.metadata.create_all(bind=database.engine)

ACCESS_TOKEN_EXPIRE_MINUTES = 3600

app = FastAPI()
# Dependency


def get_db():
    db = None
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
auth = HTTPBearer()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = decode_access_token(data=token)
        username: str = payload.get('username')
        level: int = payload.get('level')
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, level=level)
    except PyJWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.get('/')
def root():
    return RedirectResponse(url='/docs/')


@app.post('/auth/login', status_code=200)
def post_login(input: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=input.username)
    if user is None:
        raise HTTPException(status_code=400, detail='Username not existed!')
    else:
        is_password_correct = crud.get_user_password(db, input)
        if is_password_correct is False:
            raise HTTPException(
                status_code=400, detail='Password is not correct!')
        else:
            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={'username': input.username, 'level': user.level}, expires_delta=access_token_expires)
            return {'status': 200, 'message': 'success', 'data': {'access_token': access_token, 'token_type': 'Bearer'}}


@app.post('/auth/register', status_code=201)
def post_register(input: schemas.UserRegister, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=input.username)
    if user:
        raise HTTPException(
            status_code=400, detail='Username has been registered!')
    return crud.post_user(db, user=input)


@app.get('/users', response_model=List[schemas.UserInfo], status_code=200)
def get_users(db: Session = Depends(get_db), authorization: HTTPBasicCredentials = Depends(auth)):
    records = db.query(models.UserTable).all()
    if records:
        return records
    else:
        raise HTTPException(status_code=404, detail='Data Not Found')
