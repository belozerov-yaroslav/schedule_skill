from ORM.SqlalchemyOperator import SqlalchemyOperator
from ORM.data.events import Event
from controllers.message import Message
from UseCases.UseCase import UseCase
from datetime import datetime


class CreateEventUC(UseCase):
    def create(self):
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