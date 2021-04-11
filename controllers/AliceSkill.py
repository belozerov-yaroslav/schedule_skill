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
    if message.is_new_session():
        sessionStorage.add_session(message.session_id())
        # новая сессия
        NewSessionUC(message).handle()
        return
    # Обрабатываем ответ пользователя.
    if sessionStorage.is_wait_for_confirm(message.session_id()):
        ConfirmAddUC(message).handle(sessionStorage)
        return
    elif had_cmd(message.get_cmd().lower(), ['создай напоминание', 'напомни мне', 'напомни']):
        try:
            event_time, event_text, event = CreateEventUC(message).create()
        except NoTimeException:
            message.set_text('Извините, я не поняла на какое время вы хотите установить напоминание')
            return
        except NoWeekDay:
            message.set_text('Извините, я не поняла на какое день вы хотите установить напоминание')
            return
        message.set_text(f'''Отличное напоминание! на {event_time}, вы хотите {event_text}?''')
        message.clear_buttons()
        message.add_buttons([Button('Да'), Button('Нет')])
        sessionStorage.set_confirm(message.session_id(), event)
        return
    elif had_cmd(message.get_cmd(), ['что у меня запланировано', 'что запланировано']):
        try:
            message.set_text('Вы хотели:\n' + '\n'.join(GetEventsUC(message).get()))
        except NoTimeException:
            message.set_text('Извините, я не поняла того, на какой день вы хотите узнать напоминания.')
        return
    elif had_cmd(message.get_cmd(), ['спасибо', 'благодарю', 'понял']):
        message.set_text(choice(['Незачто', 'Обращайтесь', 'Всегда готова вам помочь']))
    elif had_cmd(message.get_cmd(), ['помощь', 'помоги', 'помоги мне', 'что говорить']):
        message.set_text(f'Чтобы создать напоминание скажите: "напомни на <дата время>, ' +
                         '<текст напоминания>", ' +
                         'обратите внимание, что обязательно вначале указать дату, ' +
                         'а потом текст, именно в таком порядке.\n' +
                         'Чтобы узнать, что вы запланировали, скажите "что запланировано на <дата>, <текст>"')
        return
    else:
        message.set_text('Я вас не поняла, пожалуйста, переформулируйте запрос')
        return


if __name__ == '__main__':
    app.run()
