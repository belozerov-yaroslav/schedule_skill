from controllers.message import Message
from ORM.SqlalchemyOperator import SqlalchemyOperator
from controllers.sessionStorage import SessionStorage


class UseCase:
    def __init__(self, message: Message, session_storage: SessionStorage):
        self.message = message
        self.repository = SqlalchemyOperator('../ORM/db/schedule.db')
        self.session_storage = session_storage
