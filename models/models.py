from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from config import DATABASE_URL

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Models
class UserORM(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(30), unique=True, nullable=False)
    secret = Column(String, nullable=False)


class MethodOfEncryptionORM(Base):
    __tablename__ = 'methods_of_encryption'
    id = Column(Integer, primary_key=True, index=True)
    caption = Column(String(30), nullable=False)
    json_params = Column(JSON, nullable=False)
    description = Column(String(1000), nullable=False)


class SessionORM(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    method_id = Column(Integer, nullable=False)
    data_in = Column(String, nullable=False)
    params = Column(JSON, nullable=False)
    data_out = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    time_op = Column(Float, nullable=False)

