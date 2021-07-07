from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt


def get_user_by_username(db: Session, username: str):
    return db.query(models.UserTable).filter(models.UserTable.username == username).first()

# Login


def get_user_password(db: Session, input: schemas.UserLogin):
    db_user_login: models.UserTable = get_user_by_username(
        db, username=input.username)
    return bcrypt.checkpw(input.password.encode('utf-8'), db_user_login.password.encode('utf-8'))


# Register


def post_user(db: Session, user: schemas.UserRegister):
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.UserTable(username=user.username, password=hashed_password,
                               first_name=user.first_name, last_name=user.last_name, email=user.email, age=user.age, level=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get Appointment


def get_appointment(db: Session):
    return db.query(models.AppointmentTable).all()
