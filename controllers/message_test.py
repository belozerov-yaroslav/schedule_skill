import pytest
from datetime import datetime


# from message import Message


class Message:
    def __init__(self, message):
        self.message = message
        self.request = message['request']
        self.meta = message['meta']
        self.session = message['session']
        self.version = message['version']
        self.text = ''
        self.tts = ''
        self.buttons = []
        self.is_end = False

    def build_response(self):
        response = {
            "version": self.message['version'],
            "session": self.message['session'],
            "response": {
                "text": self.text,
                "tts": self.tts,
                "end_session": self.is_end
            }
        }
        if self.tts:
            response["tts"] = self.tts
        if self.buttons:
            response["buttons"] = self.buttons
        return response

    def get_cmd(self):
        return self.request['command']

    def get_orig_text(self):
        return self.request['original_utterance']

    def is_dangerous(self):
        return self.request['markup']['dangerous_context']

    def get_datetime(self):
        entities = self.request['nlu']['entities']
        for i in entities:
            if i['type'] == 'YANDEX.DATETIME':  # если API нашли какую-то дату
                dt = i
                break
        else:  # нет даты, бросаем ошибку
            raise NoTimeException
        now = datetime.now()  # переменная используется(не верить IDE)
        args = []
        for i in ['year', 'month', 'day', 'hour', 'minute', 'second']:
            if dt['value'].get(i, 0) != 0:
                if dt['value'][i + '_is_relative']:
                    args.append(eval(f'now.{i} + dt["value"][i]'))
                else:
                    args.append(dt['value'][i])
            else:
                args.append(eval(f'now.{i}'))
        return datetime(*args)

    def user_id(self):
        return self.session['user_id']

    def is_new_session(self):
        return self.session['new']

    def set_text(self, text: str):
        self.text = text

    def set_tts(self, tts: str):
        self.tts = tts

    def buttons(self, buttons: list):
        self.buttons = buttons

    def set_is_end(self, is_end):
        self.is_end = is_end

    def split_by_date(self):
        entities = self.request['nlu']['entities']
        for i in entities:
            if i['type'] == 'YANDEX.DATETIME':  # если API нашли какую-то дату
                dt = i
                break
        else:  # нет даты, бросаем ошибку
            return self.get_cmd()
        return [self.request['nlu']['tokens'][:int(dt['tokens']['start'])]] + \
               [self.request['nlu']['tokens'][int(dt['tokens']['start']):int(dt['tokens']['end'])]] + \
               [self.request['nlu']['tokens'][int(dt['tokens']['end']):]]


message = \
    {
        "meta": {
            "locale": "ru-RU",
            "timezone": "UTC",
            "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
            "interfaces": {
                "screen": {},
                "payments": {},
                "account_linking": {}
            }
        },
        "session": {
            "message_id": 1,
            "session_id": "9c9f2b30-fea8-44cb-b97c-f00b92c6b3c3",
            "skill_id": "d04036d7-1f73-485f-8d61-6fb17a0f93fb",
            "user": {
                "user_id": "0C7C555F54F6F57FFF2B76477798F38753C2F6D8D9C5EF90FC956826A0C2BC31"
            },
            "application": {
                "application_id": "19C9AE26BF1748A3E96A9C8388B87AD1F57AE36E4C9EBC32940F8A056E15D274"
            },
            "new": False,
            "user_id": "19C9AE26BF1748A3E96A9C8388B87AD1F57AE36E4C9EBC32940F8A056E15D274"
        },
        "request": {
            "command": "алиса, создай напоминание на 10 апреля купить сырков",
            "original_utterance": "алиса создай напоминание на 10 апреля купить сырков",
            "nlu": {
                "tokens": [
                    "алиса",
                    "создай",
                    "напоминание",
                    "на",
                    "10",
                    "апреля",
                    "купить",
                    "сырков"
                ],
                "entities": [
                    {
                        "type": "YANDEX.FIO",
                        "tokens": {
                            "start": 0,
                            "end": 1
                        },
                        "value": {
                            "first_name": "алиса"
                        }
                    },
                    {
                        "type": "YANDEX.NUMBER",
                        "tokens": {
                            "start": 4,
                            "end": 5
                        },
                        "value": 10
                    },
                    {
                        "type": "YANDEX.DATETIME",
                        "tokens": {
                            "start": 4,
                            "end": 6
                        },
                        "value": {
                            "month": 4,
                            "day": 10,
                            "month_is_relative": False,
                            "day_is_relative": False
                        }
                    }
                ],
                "intents": {}
            },
            "markup": {
                "dangerous_context": False
            },
            "type": "SimpleUtterance"
        },
        "version": "1.0"
    }
mes = Message(message=message)


def build():
    print(mes.build_response())


build()


def test_cmd():
    assert mes.get_cmd() == "алиса, создай напоминание на 10 апреля купить сырков"


def test_orig():
    assert mes.get_orig_text() == "алиса создай напоминание на 10 апреля купить сырков"


def test_is_dangerous():
    assert not mes.is_dangerous()


def test_time():
    now = datetime.now()
    assert mes.get_datetime() == datetime(2021, 4, 10, now.hour, now.minute, now.second)


def test_split():
    assert mes.split_by_date() == [["алиса", "создай", "напоминание", "на"], ["10", "апреля"], ["купить", "сырков"]]
    print(mes.split_by_date())


test_split()