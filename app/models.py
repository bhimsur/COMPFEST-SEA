from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import column_property
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
    fullname = column_property(first_name + ' ' + last_name)


class AppointmentTable(Base):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_name = Column(String)
    description = Column(String)


class PatientTable(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    appointment_id = Column(Integer)
