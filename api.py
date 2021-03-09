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


class AliceBot:
    # Задаем параметры приложения Flask.
    @app.route('/p')
    def p(self):
        return 'Hello'


    @app.route("/", methods=['POST'])
    def main(self):
        # Функция получает тело запроса и возвращает ответ.
        logging.info('Request: %r', request.json)

        response = {
            "version": request.json['version'],
            "session": request.json['session'],
            "response": {
                "end_session": False
            }
        }

        self.handle_dialog(request.json, response)

        logging.info('Response: %r', response)

        return json.dumps(
            response,
            ensure_ascii=False,
            indent=2
        )

    # Функция для непосредственной обработки диалога.
    def handle_dialog(self, req, res):
        user_id = req['session']['user_id']

        if req['session']['new']:
            # Это новый пользователь.
            # Инициализируем сессию и поприветствуем его.

            sessionStorage[user_id] = {
                'suggests': [
                    "Не хочу.",
                    "Не буду.",
                    "Отстань!",
                ]
            }

            res['response'][
                'text'] = f'Привет! Купи слона! {"создатель" if user_id == "19C9AE26BF1748A3E96A9C8388B87AD1F57AE36E4C9EBC32940F8A056E15D274" else ""}'
            res['response']['buttons'] = self.get_suggests(user_id)
            return

        # Обрабатываем ответ пользователя.
        if req['request']['original_utterance'].lower() in [
            'ладно',
            'куплю',
            'покупаю',
            'хорошо',
        ]:
            # Пользователь согласился, прощаемся.
            res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
            return

        # Если нет, то убеждаем его купить слона!
        res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
            req['request']['original_utterance']
        )
        res['response']['buttons'] = self.get_suggests(user_id)

    # Функция возвращает две подсказки для ответа.
    def get_suggests(self, user_id):
        session = sessionStorage[user_id]

        # Выбираем две первые подсказки из массива.
        suggests = [
            {'title': suggest, 'hide': True}
            for suggest in session['suggests'][:2]
        ]

        # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
        session['suggests'] = session['suggests'][1:]
        sessionStorage[user_id] = session

        # Если осталась только одна подсказка, предлагаем подсказку
        # со ссылкой на Яндекс.Маркет.
        if len(suggests) < 2:
            suggests.append({
                "title": "Ладно",
                "url": "https://market.yandex.ru/search?text=слон",
                "hide": True
            })

        return suggests
