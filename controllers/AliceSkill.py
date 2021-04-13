# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
from exceptions import *
from message import Message
from UseCases.NewSessionUC import NewSessionUC
from UseCases.CreateEventUC import CreateEventUC
from UseCases.GetEventsUC import GetEventsUC
from UseCases.ConfirmAddUC import ConfirmAddUC
from UseCases.SendMessageUC import SendMessageUC
from controllers.sessionStorage import SessionStorage
from controllers.button import Button
from controllers.had_cmd import had_cmd
from random import choice
import json
import logging
from flask import Flask, request
from datetime import datetime

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
    if message.is_new_session():
        sessionStorage.add_session(message.session_id())
        # новая сессия
        NewSessionUC(message, sessionStorage).handle()
        return
    # Обрабатываем ответ пользователя.
    if sessionStorage.is_wait_for_confirm(message.session_id()):
        ConfirmAddUC(message, sessionStorage).handle(sessionStorage)
        return
    elif had_cmd(message.get_cmd().lower(), ['создай напоминание', 'напомни мне', 'напомни']):
        CreateEventUC(message, sessionStorage).create()
        return
    elif had_cmd(message.get_cmd(), ['что у меня запланировано', 'что запланировано', 'что']):
        GetEventsUC(message, sessionStorage).get()
        return
    elif had_cmd(message.get_cmd(), ['спасибо', 'благодарю', 'понял']):
        message.set_text(choice(['Незачто', 'Обращайтесь', 'Всегда готова вам помочь']))
    elif had_cmd(message.get_cmd(), ['помощь', 'помоги', 'помоги мне', 'что говорить']):
        SendMessageUC(message, sessionStorage).help()
        return
    else:
        SendMessageUC(message, sessionStorage).not_understand()
        return


if __name__ == '__main__':
    app.run()
