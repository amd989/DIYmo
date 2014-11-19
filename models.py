from flask import json

__author__ = 'Alejandro'
from peewee import *

# configuration
DATABASE = '/switches.db'
db = SqliteDatabase(DATABASE, threadlocals=True)


class BaseModel(Model):

    def json(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = getattr(self, k)
            except:
                r[k] = json.dumps(getattr(self, k))
        return r

    class Meta:
        database = db


class Switch(BaseModel):
    id = PrimaryKeyField(index=True)
    pin = IntegerField(unique=True)
    title = CharField()
    description = TextField()
    state = BooleanField()


db.connect()
#db.drop_table([Switch])
#db.create_tables([Switch])