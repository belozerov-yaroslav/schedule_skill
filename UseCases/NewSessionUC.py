from ORM.SqlalchemyOperator import SqlalchemyOperator
from controllers.message import Message


class NewSessionUC:
    def __init__(self, message: Message):
        self.message = message
        self.repository = SqlalchemyOperator('../ORM/db/schedule.db')

    def new_user(self):
        self.message.set_text(f'Привет! Ты можешь создать напоминание с помощью команды ' +
                              '"Алиса, создай напоминание на дата время, текст напоминания"')
        self.repository.add_user(self.message.user_id())

    def old_user(self):
        self.message.set_text('Здравствуй, Я тебя слушаю...')
        self.repository.update_user_info(self.repository.get_user(self.message.user_id()))

    def handle(self):
        if self.repository.user_is_created(self.message.user_id()):
            self.old_user()
        else:
            self.new_user()
