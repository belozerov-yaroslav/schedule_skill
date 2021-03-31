from ORM.SqlalchemyOperator import SqlalchemyOperator
from controllers.message import Message
from UseCases.UseCase import UseCase
from datetime import datetime


class GetEventsUC(UseCase):
    def get(self):
        user = self.repository.get_user(self.message.user_id())
        events = self.repository.get_user_events(user)
        return self.get_by_date(events)

    def get_by_date(self, events):
        return list(map(lambda x: x.text, self.simple_periodicity(events) + self.periodicity_by_weekday(events)))

    def periodicity_by_weekday(self, events):
        date = self.message.get_datetime()
        needed_events_by_weekday = filter(lambda x: x.periodicity == 2 and
                                                    date.weekday ==
                                                    int(self.repository.get_event_description(x).text) - 1,
                                          events)
        return list(needed_events_by_weekday)

    def simple_periodicity(self, events):
        date = self.message.get_datetime()
        needed_events_by_date = filter(lambda x: x.periodicity == 0 and
                                                 x.date.day == date.day and
                                                 x.date.month == date.month and
                                                 x.date.year == date.year, events)
        return list(needed_events_by_date)
