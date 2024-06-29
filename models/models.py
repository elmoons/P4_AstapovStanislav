# models.py
from sqlalchemy import Table, Column, Integer, String, JSON, DateTime, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String(30), nullable=False, unique=True),
    Column("secret", String, nullable=False)
)

methods_of_encryption = Table(
    "methods_of_encryption",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("caption", String(30), nullable=False),
    Column("json_params", JSON, nullable=False),
    Column("description", String(1000), nullable=False)
)
sessions = Table(
    "sessions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("method_id", Integer, nullable=False),
    Column("data_in", String, nullable=False),
    Column("params", JSON, nullable=False),
    Column("data_out", String, nullable=False),
    Column("status", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("time_op", Float, nullable=False)  # Используем sa.Float() для указания типа
)