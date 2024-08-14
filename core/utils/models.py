from peewee import *
from datetime import datetime

db = PostgresqlDatabase(
    "users",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432,
)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_name = CharField(max_length=255)
    first_name = CharField(max_length=255)


class Request(BaseModel):
    user = ForeignKeyField(User, backref="requests", on_delete="CASCADE")
    request_text = TextField()
    request_time = DateTimeField(default=datetime.now)


db.connect()
db.create_tables([User, Request])
