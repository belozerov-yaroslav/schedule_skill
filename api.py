# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

from exceptions import *
from controllers.message import Message
from UseCases.NewSessionUC import NewSessionUC
from UseCases.CreateEventUC import CreateEventUC
from UseCases.GetEventsUC import GetEventsUC

# Импортируем модули для работы с JSON и логами.
import json
import logging

from datetime import datetime

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}


@app.route('/post')
def post():
    return 'ONLINE!!!'


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
        # новая сессия
        NewSessionUC(message).handle()
        return

    # Обрабатываем ответ пользователя.
    if message.get_cmd().lower().startswith('алиса создай напоминание'):
        try:
            event_time, event_text = CreateEventUC(message).create()
        except NoTimeException:
            message.set_text('Извините, я не поняла на какое время вы хотите установить напоминание')
            return
        message.set_text(f'''Отличное напоминание! на {event_time.strftime("%d/%m/%Y, %H:%M:%S")}
        вы хотите {event_text}?''')
        return
    elif message.get_cmd().startswith('алиса что у меня запланировано'):
        try:
            message.set_text('Вы хотели:\n' + '\n'.join(GetEventsUC(message).get()))
        except NoTimeException:
            message.set_text('Извините, я не поняла того, на какой день вы хотите узнать напоминания.')
        return
    elif message.get_cmd().startswith('спасибо'):
        message.set_text('Незачто')
    else:
        message.set_text('Я вас не поняла, пожалуйста, переформулируйте запрос')
        message.set_tts('Я вас не поняла, пожалуйста, переформулируйте запрос')
        return


if __name__ == '__main__':
    app.run()
