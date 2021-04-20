from random import choice

from UseCases.UseCase import UseCase


class NewSessionUC(UseCase):
    # загрузка подсказок
    with open('../UseCases/tips.txt', encoding='utf8') as file:
        tips = list(map(lambda tip: tip.strip(), file.readlines()))

    def new_user(self):  # приветствие пользователя и добавление в дб
        self.message.set_text('''Привет! Вы можете создать напоминание с помощью команды
                              "Алиса, создай напоминание на дата время, текст напоминания"
                              Если вы хотите узнать, что у вас запланировано на день, то попросите:
                            "Алиса, что у меня запланировано на дата"''')
        self.repository.add_user(self.message.user_id())

    def old_user(self):  # Приветсвие с подсказкой и обновление информации о пользователе
        self.message.set_text(f'Здравствуйте. {choice(self.tips)} Я вас слушаю...')
        self.repository.update_user_info(self.repository.get_user(self.message.user_id()))

    def handle(self):  # обработка пользователя
        try:
            user_is_created = self.repository.user_is_created(self.message.user_id())
        except KeyError:  # api поддерживают анонимных пользователей
            self.message.set_text('''Извините, этот навык не поддерживает работу с анонимными пользователями, 
            пожалуйста, автроизуйтесь в учетной записи и возращайтесь.''')
            self.message.set_is_end(True)  # заканчиваем сессию
            return
        self.session_storage.add_session(self.message.session_id())  # добавляем сессию
        if user_is_created:
            self.old_user()
        else:
            self.new_user()
