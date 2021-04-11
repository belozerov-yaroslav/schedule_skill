from controllers.button import Button
from controllers.sessionStorage import SessionStorage
from UseCases.UseCase import UseCase
from controllers.had_cmd import had_cmd


class ConfirmAddUC(UseCase):
    def handle(self, session_storage: SessionStorage):
        if had_cmd(self.message.get_cmd(), ['алиса да', 'да']):
            self.message.set_text('Напоминание добавлено.')
            session_storage.delete_confirm(self.message.session_id())
        elif had_cmd(self.message.get_cmd(), ['алиса нет', 'нет']):
            self.message.set_text('Напоминание отменено.')
            self.repository.delete_user_event(session_storage.get_confirm_event(self.message.session_id()))
            session_storage.delete_confirm(self.message.session_id())
        else:
            self.message.set_text('Пожалуйста, подтвердите добавление напоминания.')
            self.message.clear_buttons()
            self.message.add_buttons([Button('Да'), Button('Нет')])
