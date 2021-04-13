import sqlalchemy
from .db_session import SqlAlchemyBase


class Notice(SqlAlchemyBase):
    __tablename__ = 'notices'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
