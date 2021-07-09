from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DB_USERNAME = config('DB_USERNAME')
DB_HOST = config('DB_HOST')
DB_PASSWORD = config('DB_PASSWORD')
DB_NAME = config('DB_NAME')

SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://' + \
    DB_USERNAME+':'+DB_PASSWORD+'@'+DB_HOST+'/'+DB_NAME

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
