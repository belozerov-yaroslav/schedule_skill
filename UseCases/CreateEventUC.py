from ORM.SqlalchemyOperator import SqlalchemyOperator
from ORM.data.events import Event
from ORM.data.event_descriptions import EventDescription
from controllers.message import Message
from UseCases.UseCase import UseCase
from datetime import datetime
from exceptions import *


class CreateEventUC(UseCase):
    def create(self):
        cmd = self.message.get_cmd().split()
        if any(map(lambda x: x in cmd, ['каждый', 'каждую', 'каждое'])):
            return self.every_week_day()
        else:
            return self.simple_event()

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
        self.repository.add_event(Event(periodicity=2, text=self.get_event_text(), date=self.message.get_datetime(),
                                        user=self.repository.get_user(self.message.user_id())),
                                  event_description=EventDescription(text=str(day_count)))
        return datetime.now(), day_count

    def simple_event(self):
        event_time = self.message.get_datetime()
        event_text = self.get_event_text()
        event = Event(date=event_time,
                      periodicity=0,
                      user=self.repository.get_user(self.message.user_id()),
                      text=event_text)
        self.save_event(event)
        return event_time, event_text

    def get_event_text(self):
        event_text = ' '.join(self.message.split_by_date()[-1])
        return event_text

    def save_event(self, event):
        self.repository.add_event(event)
