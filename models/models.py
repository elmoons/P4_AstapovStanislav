from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Interval

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String, nullable=False),
    Column("secret", String, nullable=False)
)

methods = Table(
    "methods",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("caption", String, nullable=False),
    Column("json_params", JSON),
    Column("description", String)
)

sessions = Table(
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("method_id", Integer, nullable=False),
    Column("data_in", String, nullable=False),
    Column("params", JSON),
    Column("data_out", String, nullable=False),
    Column("status", Integer, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("time_op", Interval)
)