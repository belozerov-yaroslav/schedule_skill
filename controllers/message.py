from exceptions import *
from datetime import datetime


class Message:
    """Обёртка для отправки и получения сообщений от api алисы"""
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
        # строит ответ к api, просто складывает все внесенные значения в dict
        response = {
            "version": self.message['version'],
            "session": self.message['session'],
            "response": {
                "text": self.text,
                "end_session": self.is_end,
            }
        }
        if self.tts:
            response['response']["tts"] = self.tts
        if self.buttons:
            response['response']["buttons"] = [dict(button) for button in self.buttons]
        return response

    def get_cmd(self):
        return self.request['command']  # возвращает команду пользователя

    def get_orig_text(self):
        return self.request['original_utterance']  # оригинальный текст пользователя

    def is_dangerous(self):
        return self.request['markup']['dangerous_context']  # призывы к насилию и тд

    def get_datetime(self):  # возращает время, которое сказал пользователь
        entities = self.request['nlu']['entities']
        for i in entities:
            if i['type'] == 'YANDEX.DATETIME':  # если API нашли какую-то дату
                dt = i
                break
        else:  # нет даты, бросаем ошибку
            raise NoTimeException
        now = datetime.now()
        now = now.replace(minute=0, second=0)  # переменная используется(не верить IDE)
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

    def user_id(self):  # id пользователя
        return self.session['user']['user_id']

    def is_new_session(self):
        return self.session['new']

    def set_text(self, text: str):
        self.text = text  # задать текст для build_response()

    def set_tts(self, tts: str):
        self.tts = tts  # задать tts для build_response()

    def add_buttons(self, buttons: list):
        self.buttons += buttons  # добавить несколько Button

    def set_is_end(self, is_end):
        self.is_end = is_end  # задать конец диалога

    def split_by_date(self):  # разбивает коману на 3 части: до даты, дата, после даты
        entities = self.request['nlu']['entities']
        for i in entities:
            if i['type'] == 'YANDEX.DATETIME':  # если API нашли какую-то дату
                dt = i
                break
        else:  # нет даты, кидаем всю строку
            return [self.get_cmd(), '', '']
        return [self.request['nlu']['tokens'][:int(dt['tokens']['start'])]] + \
               [self.request['nlu']['tokens'][int(dt['tokens']['start']):int(dt['tokens']['end'])]] + \
               [self.request['nlu']['tokens'][int(dt['tokens']['end']):]]

    def session_id(self):
        return self.session['session_id']

    def add_button(self, button):
        self.buttons.append(button)

    def clear_buttons(self):
        self.buttons = []

    def timezone(self):  # часовой пояс
        return self.meta['timezone']

    def has_time(self):
        try:
            self.get_datetime()
        except NoTimeException:
            return False
        return True
