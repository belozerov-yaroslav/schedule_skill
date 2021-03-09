# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

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

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        res['response']['text'] = f'Привет! Ты можешь создать напоминание с помощью команды ' + \
                                  '"Алиса, создай напоминание на дата время, текст напоминания"'
        return

    # Обрабатываем ответ пользователя.
    if req['request']['command'].lower().startwith('алиса создай напоминание'):
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Отличное напоминание!'
        print('создать напоминание:', req['request']['command'][24:])
        return
    else:
        res['response']['text'] = 'Я вас не поняла, пожалуйста, переформулируйте запрос'
