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


class AppointmentBase(BaseModel):
    description: str
    doctor_name: str


class AppointmentInfo(AppointmentBase):
    id: int

    class Config:
        orm_mode = True


class PatientUser(BaseModel):
    user_id: int


class PatientBase(PatientUser):
    appointment_id: int


class PatientInfo(PatientBase):
    id: int

    class Config:
        orm_mode = True
