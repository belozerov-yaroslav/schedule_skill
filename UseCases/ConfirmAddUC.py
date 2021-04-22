from UseCases.UseCase import UseCase
from controllers.button import Button
from controllers.sessionStorage import SessionStorage
from controllers.had_cmd import had_cmd


class ConfirmAddUC(UseCase):
    # обрабатывает ответы пользователя на просьбу подтвердить добавление event
    # event по-умолчанию добавлен, есои согласен, то ничего не делаем, иначе удаляем
    def handle(self, session_storage: SessionStorage):  # обработчик
        if had_cmd(self.message.get_cmd(), ['да']):  # согласен, удаляем отслеживание
            self.message.set_text('Напоминание добавлено.')
            session_storage.delete_confirm(self.message.session_id())
        elif had_cmd(self.message.get_cmd(), ['нет']):  # отменяет, удаляем event, удаляем отслеживание
            self.message.set_text('Напоминание отменено.')
            event = self.repository.get_event_by_id(self.session_storage.get_confirm_event(
                self.message.session_id()))
            self.repository.delete_user_event(event)
            session_storage.delete_confirm(self.message.session_id())
        else:  # неправильная команда, просим повторить и обновляем кнопки
            self.message.set_text('Пожалуйста, подтвердите добавление напоминания.')
            self.message.clear_buttons()
            self.message.add_buttons([Button('Да'), Button('Нет')])
