from controllers.message import Message
from ORM.SqlalchemyOperator import SqlalchemyOperator


class UseCase:
    def __init__(self, message: Message, session_storage):
        self.message = message
        self.repository = SqlalchemyOperator('../ORM/db/schedule.db')
        self.session_storage = session_storage
