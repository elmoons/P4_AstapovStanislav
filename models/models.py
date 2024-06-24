from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String, nullable=False),
    Column("secret", String, nullable=False)
)