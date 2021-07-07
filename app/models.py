from sqlalchemy import Column, Integer, String
from app.database import Base


class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
    level = Column(Integer)


class DoctorTable(Base):
    __tablename__ = 'doctor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_name = Column(String)


class AppointmentTable(Base):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer)
    description = Column(String)
    user_id = Column(String)
