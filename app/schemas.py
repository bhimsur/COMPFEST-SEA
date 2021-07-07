from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserLogin(UserBase):
    password: str


class UserInfo(UserBase):
    id: int
    level: int
    email: str
    username: str

    class Config:
        orm_mode = True


class UserRegister(UserLogin):
    first_name: str
    last_name: str
    age: int
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    level: int = 1


class DoctorBase(BaseModel):
    doctor_name: str


class DoctorInfo(DoctorBase):
    id: int

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    description: str


class AppointmentDoctor(AppointmentBase):
    doctor_id: int


class AppointmentUser(AppointmentBase):
    user_id: int


class AppointmentInfo(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
