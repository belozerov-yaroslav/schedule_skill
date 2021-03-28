from ORM.SqlalchemyOperator import SqlalchemyOperator
from controllers.message import Message
from UseCases.UseCase import UseCase


class GetEventsUC(UseCase):
    def get(self):
        user = self.repository.get_user(self.message.user_id())
        events = self.repository.get_user_events(user)
        return self.get_by_date(events)

    def get_by_date(self, events):
        date = self.message.get_datetime()
        needed_events = map(lambda event: event.text, filter(lambda x: x.periodicity == 0 and
                                                                       x.date.day == date.day and
                                                                       x.date.month == date.month and
                                                                       x.date.year == date.year, events))
        return list(needed_events)
