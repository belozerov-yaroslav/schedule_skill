# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

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
    if req['request']['command'].lower().startswith('алиса создай напоминание'):

        dt = {"value": {"day": 1, "day_is_relative": True}}  # default
        entities = req['request']['nlu']['entities']
        for i in entities:
            if i['type'] == 'YANDEX.DATETIME':  # если API нашли какую-то дату
                dt = i
                break
        now = datetime.now()
        args = []
        for i in ['year', 'month', 'day', 'hour', 'minute', 'second']:
            if dt['value'].get(i, 0) != 0:
                if dt['value'][i + '_is_relative']:
                    print(eval(f'now.{i}'))
                    print(dt["value"][i])
                    args.append(eval(f'now.{i} + dt["value"][i]'))

                else:
                    args.append(dt['value'][i])
            else:
                args.append(eval(f'now.{i}'))
        n = datetime(*args)
        print(now)
        print(n)
        res['response']['text'] = f'Отличное напоминание! на {n.strftime("%m/%d/%Y, %H:%M:%S")}'
        print('создать напоминание:', req['request']['command'][24:])
        return
    else:
        res['response']['text'] = 'Я вас не поняла, пожалуйста, переформулируйте запрос'
        return