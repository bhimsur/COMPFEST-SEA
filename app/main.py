from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from starlette.responses import RedirectResponse


from app import schemas, models, database, crud
from app.utils import decode_access_token, create_access_token

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()
# Dependency


def get_db():
    db = None
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


auth = HTTPBearer()


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
            access_token = create_access_token(
                data={'username': input.username, 'level': user.level})
            return {'status': 200, 'message': 'success', 'data': {'access_token': access_token, 'token_type': 'Bearer'}}


@app.post('/auth/register', status_code=201)
def post_register(input: schemas.UserRegister, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=input.username)
    if user:
        raise HTTPException(
            status_code=400, detail='Username has been registered!')
    return crud.post_user(db, user=input)


def get_user_level(authorization: HTTPBasicCredentials = Depends(auth)):
    payload = decode_access_token(data=authorization.credentials)
    return payload


@app.get('/users', status_code=200)
def get_users(db: Session = Depends(get_db), authorization: schemas.UserInfo = Depends(get_user_level)):
    if authorization['data']['level'] == 0:
        return {'status': 200, 'message': 'success', 'data': 'user tidak diperbolehkan'}
    else:
        records = db.query(models.UserTable).all()
        if records:
            return records
        else:
            raise HTTPException(status_code=404, detail='Data Not Found')
