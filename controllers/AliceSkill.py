# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
from message import Message
# импорт UseCase
from UseCases.NewSessionUC import NewSessionUC
from UseCases.CreateEventUC import CreateEventUC
from UseCases.GetEventsUC import GetEventsUC
from UseCases.ConfirmAddUC import ConfirmAddUC
from UseCases.SendMessageUC import SendMessageUC
from UseCases.DeleteEventUC import DeleteEventUC
# импорт controllers
from controllers.sessionStorage import SessionStorage
from controllers.button import Button
from controllers.had_cmd import had_cmd

from random import choice
import json
import logging
from flask import Flask, request

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
    message.add_button(Button('Помощь'))
    if message.is_new_session():  # новая сессия
        NewSessionUC(message, sessionStorage).handle()
        return
    # Обрабатываем ответ пользователя.
    if sessionStorage.is_wait_for_confirm(message.session_id()):  # ждем подтверждения добавления event
        ConfirmAddUC(message, sessionStorage).handle(sessionStorage)
        return
    elif sessionStorage.is_wait_for_delete(message.session_id()):  # ждем выбора event для удаления
        DeleteEventUC(message, sessionStorage).delete()
        return
    # had_cmd - функция проверяет начинается ли команда со строки или с "алиса" + строка
    elif had_cmd(message.get_cmd().lower(), ['создай напоминание', 'напомни мне', 'напомни']):
        CreateEventUC(message, sessionStorage).create()  # создать напоминание
        return
    elif had_cmd(message.get_cmd(), ['что у меня запланировано', 'что запланировано', 'что']):
        GetEventsUC(message, sessionStorage).get()  # вывод списка event
        return
    elif had_cmd(message.get_cmd(), ['удалить на', 'удали на', 'хочу удалить на']):
        DeleteEventUC(message, sessionStorage).delete()  # вывод списка для выбора нужного на удаление
        return
    elif had_cmd(message.get_cmd(), ['спасибо', 'благодарю', 'понял']):
        message.set_text(choice(['Незачто', 'Обращайтесь', 'Всегда готова вам помочь']))
    elif had_cmd(message.get_cmd(), ['помощь', 'помоги', 'помоги мне', 'что говорить']):
        SendMessageUC(message, sessionStorage).help()  # отправляем стандартную реплику
        return
    else:
        SendMessageUC(message, sessionStorage).not_understand()  # отправляем стандартную реплику
        return


if __name__ == '__main__':
    app.run(host='0.0.0.0')
