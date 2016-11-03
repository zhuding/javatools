# coding=utf8

from app import db
from app.helpers.helpers import *

'''
Base model
'''
class Base(db.Model):
	__abstract__ = True
	id = db.Column(db.Integer, primary_key=True)
