# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

from exceptions import *
from message import Message

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
        # Это новая сессия

        message.set_text(f'Привет! Ты можешь создать напоминание с помощью команды ' +
                         '"Алиса, создай напоминание на дата время, текст напоминания"')
        return

    # Обрабатываем ответ пользователя.
    if message.get_cmd().lower().startswith('алиса создай напоминание'):
        try:
            time = message.get_datetime()
        except NoTimeException:
            message.set_text('Извините, я не поняла на какое время вы хотите установить напоминание')
            return
        message.set_text(f'Отличное напоминание! на {time.strftime("%m/%d/%Y, %H:%M:%S")}')
        return
    else:
        message.set_text('Я вас не поняла, пожалуйста, переформулируйте запрос, да да')
        message.set_tts('Я вас не поняла, пожалуйста, переформулируйте запрос')
        return


if __name__ == '__main__':
    app.run()
