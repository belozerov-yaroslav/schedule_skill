from datetime import datetime, timedelta
import csv
from exceptions import *


def get_utc_time(time: datetime, time_zone):
    delta = timedelta(hours=get_utc_diff(time_zone))
    new_time = time - delta
    return new_time


def get_zone_time(time: datetime, time_zone):
    delta = timedelta(hours=get_utc_diff(time_zone))
    new_time = time + delta
    return new_time


def get_utc_diff(time_zone):
    inf = {}
    with open('../UseCases/times.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f, delimiter=';')
        for i in reader:
            if i:
                inf[i[2]] = int(i[5][1:3].replace('в€’', '-')) * 1 if i[5][0] == '+' else -1
    try:
        return inf[time_zone]
    except KeyError:
        raise WrongTimezone


if __name__ == '__main__':
    print(get_utc_time(datetime.now(), 'Asia/Yekaterinburg').strftime('%d/%m/%Y, %H:%M:%S'))
