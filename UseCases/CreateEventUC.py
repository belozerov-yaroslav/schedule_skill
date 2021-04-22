from UseCases.UseCase import UseCase
from UseCases.utc_time import get_utc_time
from controllers.button import Button
from ORM.data.events import Event
from ORM.data.event_descriptions import EventDescription
from exceptions import *


class CreateEventUC(UseCase):
    # создает event и устанавливает ожидание подтверждения
    def create(self):  # определяет тип напоминания и включает отслеживание
        cmd = self.message.get_cmd().split()
        try:
            if any(map(lambda x: x in cmd, ['каждый', 'каждую', 'каждое'])):
                event_time, event_text, event_id = self.every_week_day()  # переодичность в днях недели
            else:
                event_time, event_text, event_id = self.simple_event()  # обычный event
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
        self.session_storage.set_confirm(self.message.session_id(), event_id)

    def every_week_day(self):  # если есть слово "каждый"
        cmd = self.message.get_cmd().split()
        for word in ['каждый', 'каждую', 'каждое']:
            if word in cmd:
                break
        week_day = cmd[cmd.index(word) + 1]  # слово дня недели
        for name, day_count in zip(['пон', 'вто', 'сре', 'чет', 'пят', 'суб', 'вос'], range(1, 8)):
            if week_day.startswith(name):
                break
        else:
            raise NoWeekDay
        event = Event(id=self.repository.get_new_id(),
                      periodicity=2,
                      text=self.get_event_text(),
                      date=self.message.get_datetime(),
                      user=self.repository.get_user(self.message.user_id()))
        event_id = event.id
        self.save_event(event,
                        event_description=EventDescription(text=str(day_count)))
        days_count = ['первый', 'второй', 'третий', 'четвёртый', 'пятый', 'шестой', 'седьмой']
        return f'каждый {days_count[day_count - 1]} день недели, ' + \
               f'{str(self.message.get_datetime().hour).rjust(2, "0")}:' + \
               f'{str(self.message.get_datetime().minute).rjust(2, "0")}', self.get_event_text(), event_id

    def simple_event(self):  # обычный event
        event_time = self.message.get_datetime()
        event_text = self.get_event_text()
        event = Event(id=self.repository.get_new_id(),
                      date=event_time,
                      periodicity=0,
                      user=self.repository.get_user(self.message.user_id()),
                      text=event_text)
        event_id = event.id
        self.save_event(event)
        return event_time.strftime("%d/%m/%Y, %H:%M:%S"), event_text, event_id

    def get_event_text(self):  # получить текст напоминания
        event_text = ' '.join(self.message.split_by_date()[-1])
        return event_text

    def save_event(self, event, event_description=None):  # сохранить event
        event.date = get_utc_time(event.date, self.message.timezone())
        self.repository.add_event(event, event_description=event_description)
