__author__ = 'Alejandro'
from peewee import *

# configuration
DATABASE = '/switches.db'
db = SqliteDatabase(DATABASE, threadlocals=True)


class BaseModel(Model):
    class Meta:
        database = db


class Switch(BaseModel):
    id = IntegerField(index=True, unique=True)
    pin = IntegerField(unique=True)
    title = CharField()
    description = TextField()
    state = BooleanField()


db.connect()
#db.create_tables([Switch])