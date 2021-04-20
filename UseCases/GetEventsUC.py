from UseCases.utc_time import get_zone_time
from UseCases.UseCase import UseCase
from datetime import datetime
from exceptions import *


class GetEventsUC(UseCase):  # выводит все event пользователя на дату
    def get(self):
        user = self.repository.get_user(self.message.user_id())
        all_events = self.repository.get_user_events(user)
        try:
            events = self.get_by_date(all_events)
        except NoTimeException:
            self.message.set_text('Извините, я не поняла того, на какой день вы хотите узнать напоминания.')
            return
        time_now = get_zone_time(datetime.now(), self.message.timezone())
        next_event = True
        send_text = 'Вы хотели:\n'
        if self.message.get_datetime().date() == time_now.date():
            for event in events:
                event.date = get_zone_time(event.date, self.message.timezone())
                if event.date.time() < time_now.time():
                    send_text += '🟢 ' + str(event) + '\n'  # event уже прошел
                if event.date.time() >= time_now.time():
                    if next_event:
                        send_text += '⚪ ' + str(event) + '\n'  # следущий event
                        next_event = False
                    else:
                        send_text += '🟡 ' + str(event) + '\n'  # event в будущем
        else:
            for event in events:
                send_text += '🟡 ' + str(event) + '\n'
        self.message.set_text(send_text.rstrip())
        return

    def get_by_date(self, events):  # получить все event на определенную дату
        return list(sorted(self.simple_periodicity(events) + self.periodicity_by_weekday(events),
                           key=lambda x: x.date))

    def periodicity_by_weekday(self, events):
        # получение всех event, которые подходят к дате по переодичности
        date = self.message.get_datetime()
        needed_events_by_weekday = filter(lambda x: x.periodicity == 2 and
                                                    int(self.repository.get_event_description(x).text) - 1 ==
                                                    date.weekday(),
                                          events)
        return list(needed_events_by_weekday)

    def simple_periodicity(self, events):  # получение все event с нужной датой
        date = self.message.get_datetime()
        needed_events_by_date = filter(lambda x: x.periodicity == 0 and
                                                 x.date.day == date.day and
                                                 x.date.month == date.month and
                                                 x.date.year == date.year, events)
        return list(needed_events_by_date)
