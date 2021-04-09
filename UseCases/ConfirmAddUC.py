from random import choice

from ORM.SqlalchemyOperator import SqlalchemyOperator
from controllers.message import Message
from controllers.sessionStorage import SessionStorage
from UseCases.UseCase import UseCase


def had_cmd(message: str, cmd_list):
    if isinstance(cmd_list, list):
        for cmd in cmd_list:
            if message.startswith(cmd):
                return True
        return False
    else:
        return message.startswith(cmd_list)


class ConfirmAddUC(UseCase):
    def handle(self, sessionStorage: SessionStorage):
        if had_cmd(self.message.get_cmd(), ['алиса да', 'да']):
            self.message.set_text('Напоминание добавлено.')
            sessionStorage.delete_confirm(self.message.session_id())
        elif had_cmd(self.message.get_cmd(), ['алиса нет', 'нет']):
            self.message.set_text('Напоминание отменено.')
            self.repository.delete_user_event(sessionStorage.get_confirm_event(self.message.session_id()))
            sessionStorage.delete_confirm(self.message.session_id())
        else:
            self.message.set_text('Пожалуйста, подтвердите добавление напоминания.')