from sqlalchemy.orm import Session
from sqlalchemy import func, update
from sqlalchemy.sql.functions import count
from sqlalchemy.util.compat import decode_backslashreplace
from app.models import UserTable, AppointmentTable, PatientTable
from app.schemas import PatientUser, UserBase, UserInfo, UserLogin, UserRegister, AppointmentInfo, AppointmentBase, PatientBase, PatientInfo
import bcrypt


def get_user_by_username(db: Session, username: str):
    return db.query(UserTable).filter(UserTable.username == username).first()

# Login


def get_user_password(db: Session, input: UserLogin):
    db_user_login: UserTable = get_user_by_username(
        db, username=input.username)
    return bcrypt.checkpw(input.password.encode('utf-8'), db_user_login.password.encode('utf-8'))


# Register


def post_user(db: Session, user: UserRegister):
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = UserTable(username=user.username, password=hashed_password,
                        first_name=user.first_name, last_name=user.last_name, email=user.email, age=user.age, level=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Appointment


def get_appointment(db: Session):
    return db.query(AppointmentTable).all()


def get_appointment_by_id(db: Session, id: int):
    return db.query(AppointmentTable).filter(AppointmentTable.id == id).first()


def get_appointment_detail(db: Session, id: int):
    query = db.query(AppointmentTable)\
        .join(PatientTable, AppointmentTable.id == PatientTable.appointment_id)\
        .join(UserTable, UserTable.id == PatientTable.user_id)\
        .filter(AppointmentTable.id == id)
    q = query.with_entities(AppointmentTable.id.label('appointment_id'),
                            func.group_concat(UserTable.last_name).label('daftar_pasien'))
    return q.first()


def post_appointment(db: Session, appointment: AppointmentInfo):
    if appointment.id is None:
        query = AppointmentTable(doctor_name=appointment.doctor_name,
                                 description=appointment.description)
        db.add(query)
        db.commit()
        db.refresh(query)
        return query
    elif appointment.id > 0:
        query = db.query(AppointmentTable).get(appointment.id)
        props = {'doctor_name': appointment.doctor_name,
                 'description': appointment.description}
        for key, value in props.items():
            setattr(query, key, value)
        db.commit()
        db.flush()
        return query


def delete_appointment_by_id(db: Session, id: int):
    query = db.query(AppointmentTable).filter(
        AppointmentTable.id == id).delete()
    db.commit()
    db.flush()
    return query


# Patient
def get_patient_by_user_id(db: Session, user_id: int):
    return db.query(PatientTable).filter(PatientTable.user_id == user_id).all()


def delete_patient_by_id(db: Session, user_id: int, id: int):
    get = get_patient_by_user_id(db, user_id)
    if len(get) != 0:
        query = db.query(PatientTable).filter(PatientTable.id == id).delete()
        db.commit()
        db.flush()
        return query
    else:
        return {}


def post_patient(db: Session, id: int, user_id: int):
    query = PatientTable(appointment_id=id,
                         user_id=user_id)
    db.add(query)
    db.commit()
    db.flush()
    return query


def get_max_appointment_by_id(db: Session, appointment_id: int):
    query = db.query(PatientTable).group_by(PatientTable.appointment_id).filter(
        PatientTable.appointment_id == appointment_id)
    q = query.with_entities(PatientTable.appointment_id.label('appointment_id'),
                            func.count(PatientTable.appointment_id).label('total_patient'))
    return q.first()
