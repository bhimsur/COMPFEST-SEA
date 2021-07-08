from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app import schemas, models, database, crud
from app.utils import decode_access_token, create_access_token

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

origins = ['*', 'http://127.0.0.1:3000']
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])


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

# Auth


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
                data={'username': input.username, 'level': user.level, 'id': user.id})
            return {'status': 200, 'message': 'success', 'data': {'access_token': access_token, 'token_type': 'Bearer', 'user_level': user.level}}


@app.post('/auth/register', status_code=201)
def post_register(input: schemas.UserRegister, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=input.username)
    if user:
        raise HTTPException(
            status_code=400, detail='Username has been registered!')
    else:
        query = crud.post_user(db, user=input)
        return {'status': 201, 'message': 'success', 'data': query} if query else {'status': 400, 'message': 'failed', 'data': {}}


def get_user_level(authorization: HTTPBasicCredentials = Depends(auth)):
    payload = decode_access_token(data=authorization.credentials)
    return payload

# Appointment


@app.get('/appointment', status_code=200)
def get_appointment(db: Session = Depends(get_db)):
    records = crud.get_appointment(db)
    return {'status': 200, 'message': 'success', 'data': records}


@app.get('/appointment/{id}', status_code=200)
def get_appointment_by_id(id: int, db: Session = Depends(get_db)):
    records = crud.get_appointment_by_id(db, id)
    return {'status': 200, 'message': 'success', 'data': records}


@app.get('/appointment/detail/{id}', status_code=200)
def get_appointment_detail(id: int, db: Session = Depends(get_db), auth: schemas.UserInfo = Depends(get_user_level)):
    if auth['data']['level'] == 0:
        return {'status': 403, 'message': 'success', 'data': 'Permission denied!'}
    else:
        query = crud.get_appointment_detail(db, id)
        return {'status': 200, 'message': 'success', 'data': query} if query else {'status': 400, 'message': 'failed', 'data': {}}


@app.post('/appointment', status_code=201)
def post_appointment(input: schemas.AppointmentBase, db: Session = Depends(get_db),  auth: schemas.UserInfo = Depends(get_user_level)):  # only admin
    if auth['data']['level'] == 0:
        return {'status': 403, 'message': 'success', 'data': 'Permission denied!'}
    else:
        query = crud.post_appointment(db, post=input)
        if query:
            return {'status': 201, 'message': 'success', 'data': query}
        else:
            return {'status': 400, 'message': 'failed', 'data': {}}


@app.post('/appointment/{id}', status_code=200)
def put_appointment(input: schemas.AppointmentInfo, db: Session = Depends(get_db), auth: schemas.UserInfo = Depends(get_user_level)):
    if auth['data']['level'] == 0:
        return {'status': 403, 'message': 'success', 'data': 'Permission denied!'}
    else:
        query = crud.post_appointment(db, appointment=input)
        if query:
            return {'status': 200, 'message': 'success', 'data': query}
        else:
            return {'status': 400, 'message': 'failed', 'data': {}}


@app.delete('/appointment/{id}')
def delete_appointment(id: int, db: Session = Depends(get_db), auth: schemas.UserInfo = Depends(get_user_level)):
    if auth['data']['level'] == 0:
        return {'status': 403, 'message': 'failed', 'data': 'Permission denied!'}
    else:
        query = crud.delete_appointment_by_id(db, id)
        return {'status': 200, 'message': 'success', 'data': id} if query else {'status': 400, 'message': 'failed', 'data': 'Appointment not found!'}

# Patient


@app.get('/patient/{user_id}', status_code=200)
def get_patient_by_user_id(db: Session = Depends(get_db), auth: schemas.UserInfo = Depends(get_user_level)):
    query = crud.get_patient_by_user_id(db, auth['data']['id'])
    return {'status': 200, 'message': 'success', 'data': query} if query else {'status': 400, 'message': 'failed!', 'data': 'Appointment not found'}


@app.delete('/patient/{id}', status_code=200)
def delete_patient_by_id(id: int, db: Session = Depends(get_db), auth: schemas.UserInfo = Depends(get_user_level)):
    query = crud.delete_patient_by_id(db, auth['data']['id'], id)
    return {'status': 200, 'message': 'success', 'data': query} if query else {'status': 400, 'message': 'failed!', 'data': 'Appointment not found'}


@app.post('/appointment/apply/{id}', status_code=200)
def post_patient(id: int, db: Session = Depends(get_db), auth: schemas.UserInfo = Depends(get_user_level)):
    query = crud.get_max_appointment_by_id(db, id)
    if query['total_patient'] == 3:
        return {'status': 400, 'message': 'failed', 'data': 'Fully booked!'}
    else:
        check = crud.get_patient_by_user_id_appointment_id(
            db, id, auth['data']['id'])
        if check:
            return {'status': 400, 'message': 'failed!', 'data': 'Already registered'}
        else:
            check = crud.get_appointment_by_id(db, id)
            if check:
                query = crud.post_patient(db, id, auth['data']['id'])
                return {'status': 200, 'message': 'success', 'data': check} if query else {'status': 400, 'message': 'failed!', 'data': 'Appointment not found'}


@app.get('/applied', status_code=200)
def get_all_applied(db: Session = Depends(get_db), auth: schemas.UserInfo = Depends(get_user_level)):
    if auth['data']['level'] == 0:
        user_id = auth['data']['id']
        query = crud.get_all_applied(db, user_id)
        return {'status': 200, 'message': 'success', 'data': query}
    else:
        return {'status': 400, 'message': 'failed', 'data': 'patient only'}
