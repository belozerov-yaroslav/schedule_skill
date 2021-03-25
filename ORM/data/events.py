import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase):
    __tablename__ = 'events'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, nullable=False)
    periodcity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    user = orm.relation('User')
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)