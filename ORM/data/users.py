import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, nullable=False)
    last_visit = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, nullable=False)
    num_of_vis = sqlalchemy.Column(sqlalchemy.Integer, default=1, nullable=False)
