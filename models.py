from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
ma = Marshmallow()
db = SQLAlchemy()


class Phone(db.Model):
    __tablename__ = 'phone_lines'

    phone_number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    minutes = db.Column(db.Integer)

    def __init__(self, phone_number, name):
        self.phone_number = phone_number
        self.name = name
        self.minutes = 0


class PhoneSchema(ma.Schema):
    phone_number = fields.Integer()
    name = fields.String()
    minutes = fields.Integer()

