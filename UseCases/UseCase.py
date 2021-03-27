from controllers.message import Message
from ORM.SqlalchemyOperator import SqlalchemyOperator


class UseCase:
    def __init__(self, message: Message):
        self.message = message
        self.repository = SqlalchemyOperator('../ORM/db/schedule.db')
