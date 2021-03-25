from exceptions import *
from datetime import datetime


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
            "text": self.text,
            "tts": self.tts,
            "response": {
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

    def get_user_id(self):
        return self.session['user_id']

    def is_new_user(self):
        return self.session['new']

    def set_text(self, text: str):
        self.text = text

    def set_tts(self, tts: str):
        self.tts = tts

    def buttons(self, buttons: list):
        self.buttons = buttons

    def set_is_end(self, is_end):
        self.is_end = is_end

