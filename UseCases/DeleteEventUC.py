from ORM.SqlalchemyOperator import SqlalchemyOperator
from ORM.data.events import Event
from ORM.data.event_descriptions import EventDescription
from controllers.message import Message
from UseCases.UseCase import UseCase
from UseCases.GetEventsUC import GetEventsUC
from controllers.button import Button
from UseCases.utc_time import get_utc_time, get_zone_time
from datetime import datetime
from exceptions import *


class DeleteEventUC(UseCase):
    def delete(self):
        try:
            if self.session_storage.is_wait_for_delete(self.message.session_id()):
                self.delete_event()
                return
            else:
                self.suggest_options()
                return
        except NoTimeException:
            self.message.set_text('Извините, я не поняла, на какое время вы хотите установить напоминание')
            return

    def suggest_options(self):
        user = self.repository.get_user(self.message.user_id())
        all_events = self.repository.get_user_events(user)
        events = GetEventsUC(self.message, self.session_storage).get_by_date(all_events)
        send_text = f'Напоминания на {self.message.get_datetime().strftime("%d/%m/%Y, %H:%M:%S")},' + \
                    ' для удаления скажите номер нужного события:\n'
        for num, event in enumerate(events):
            send_text += str(num + 1) + ' : ' + str(event) + '\n'
        self.message.set_text(send_text.rstrip())
        self.session_storage.set_delete(self.message.session_id(), events)
        self.message.clear_buttons()
        self.message.add_buttons([Button(str(i + 1)) for i in range(len(events))] + [Button('Отмена')])
        return

    def delete_event(self):
        events = self.session_storage.delete_events(self.message.session_id())
        if self.message.get_cmd() in [str(i + 1) for i in range(len(events))]:
            delete_event = events[int(self.message.get_cmd()) - 1]
            self.message.set_text('Событие: ' + str(delete_event) + ' удалено')
            self.repository.delete_user_event(delete_event)
            self.session_storage.delete_wait_delete(self.message.session_id())
        elif self.message.get_cmd() == 'отмена':
            self.message.set_text('Удаление отменено')
            self.session_storage.delete_wait_delete(self.message.session_id())
        else:
            self.message.clear_buttons()
            self.message.add_buttons([Button(str(i + 1)) for i in range(len(events))] + [Button('Отмена')])
            self.message.set_text('Пожалуйста, укажите номер нужного напоминания.')

