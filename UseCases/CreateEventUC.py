from ORM.SqlalchemyOperator import SqlalchemyOperator
from ORM.data.events import Event
from ORM.data.event_descriptions import EventDescription
from controllers.message import Message
from UseCases.UseCase import UseCase
from controllers.button import Button
from UseCases.utc_time import get_utc_time
from datetime import datetime
from exceptions import *


class CreateEventUC(UseCase):
    def create(self):
        cmd = self.message.get_cmd().split()
        try:
            if any(map(lambda x: x in cmd, ['каждый', 'каждую', 'каждое'])):
                event_time, event_text, event = self.every_week_day()
            else:
                event_time, event_text, event = self.simple_event()
        except NoWeekDay:
            self.message.set_text('Извините, я не поняла, на какой день вы хотите установить напоминание')
            return
        except NoTimeException:
            self.message.set_text('Извините, я не поняла, на какое время вы хотите установить напоминание')
            return
        except WrongTimezone:
            self.message.set_text('Извините, я не поняла в каком часовом поясе вы находитесь и не могу' +
                                  ' установить напоминание :(')
            return
        self.message.set_text(f'''Отличное напоминание! на {event_time}, вы хотите {event_text}?''')
        self.message.clear_buttons()
        self.message.add_buttons([Button('Да'), Button('Нет')])
        self.session_storage.set_confirm(self.message.session_id(), event)

    def every_week_day(self):
        cmd = self.message.get_cmd().split()
        for word in ['каждый', 'каждую', 'каждое']:
            if word in cmd:
                break
        week_day = cmd[cmd.index(word) + 1]
        for name, day_count in zip(['пон', 'вто', 'сре', 'чет', 'пят', 'суб', 'вос'], range(1, 8)):
            if week_day.startswith(name):
                break
        else:
            raise NoWeekDay
        event = Event(periodicity=2, text=self.get_event_text(), date=self.message.get_datetime(),
                      user=self.repository.get_user(self.message.user_id()))
        self.save_event(event,
                        event_description=EventDescription(text=str(day_count)))
        return f'каждый {day_count} день, {str(self.message.get_datetime().hour).rjust(2, "0")}:' + \
               f'{str(self.message.get_datetime().minute).rjust(2, "0")}', self.get_event_text(), event  # TODO __str__

    def simple_event(self):
        event_time = self.message.get_datetime()
        event_text = self.get_event_text()
        event = Event(date=event_time,
                      periodicity=0,
                      user=self.repository.get_user(self.message.user_id()),
                      text=event_text)
        self.save_event(event)
        return event_time.strftime("%d/%m/%Y, %H:%M:%S"), event_text, event

    def get_event_text(self):
        event_text = ' '.join(self.message.split_by_date()[-1])
        return event_text

    def save_event(self, event, event_description=None):
        event.date = get_utc_time(event.date, self.message.timezone())
        print(event)
        self.repository.add_event(event, event_description=event_description)
