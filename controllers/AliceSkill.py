# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
from exceptions import *
from message import Message
from UseCases.NewSessionUC import NewSessionUC
from UseCases.CreateEventUC import CreateEventUC
from UseCases.GetEventsUC import GetEventsUC
from UseCases.ConfirmAddUC import ConfirmAddUC
from controllers.sessionStorage import SessionStorage
import json
import logging
from datetime import datetime
from flask import Flask, request


def had_cmd(message: str, cmd_list):
    if isinstance(cmd_list, list):
        for cmd in cmd_list:
            if message.startswith(cmd):
                return True
        return False
    else:
        return message.startswith(cmd_list)


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = SessionStorage()


@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)
    message = Message(request.json)

    handle_dialog(message)

    logging.info('Response: %r', message.build_response())

    return json.dumps(
        message.build_response(),
        ensure_ascii=False,
        indent=2
    )


# Функция для непосредственной обработки диалога.
def handle_dialog(message):
    if message.is_new_session():
        sessionStorage.add_session(message.session_id())
        # новая сессия
        NewSessionUC(message).handle()
        return
    # Обрабатываем ответ пользователя.
    if sessionStorage.is_wait_for_confirm(message.session_id()):
        ConfirmAddUC(message).handle(sessionStorage)
        return
    if had_cmd(message.get_cmd().lower(), ['алиса создай напоминание', 'создай напоминание']):
        try:
            event_time, event_text, event = CreateEventUC(message).create()
        except NoTimeException:
            message.set_text('Извините, я не поняла на какое время вы хотите установить напоминание')
            return
        except NoWeekDay:
            message.set_text('Извините, я не поняла на какое день вы хотите установить напоминание')
            return
        message.set_text(f'''Отличное напоминание! на {event_time}, вы хотите {event_text}?''')
        sessionStorage.set_confirm(message.session_id(), event)
        return
    elif had_cmd(message.get_cmd(), ['алиса что у меня запланировано', 'что у меня запланировано',
                                     'что запланировано']):
        try:
            message.set_text('Вы хотели:\n' + '\n'.join(GetEventsUC(message).get()))
        except NoTimeException:
            message.set_text('Извините, я не поняла того, на какой день вы хотите узнать напоминания.')
        return
    elif had_cmd(message.get_cmd(), ['спасибо', 'благодарю', 'понял']):
        message.set_text('Незачто')
    else:
        message.set_text('Я вас не поняла, пожалуйста, переформулируйте запрос')
        return


if __name__ == '__main__':
    app.run()
