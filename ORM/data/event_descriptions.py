import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class EventDescription(SqlAlchemyBase):
    __tablename__ = 'event_descriptions'

    event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('events.id'),
                                 primary_key=True, nullable=False)
    event = orm.relation('Event')
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)