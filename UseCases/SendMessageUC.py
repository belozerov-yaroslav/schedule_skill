from UseCases.UseCase import UseCase


class SendMessageUC(UseCase):
    def not_understand(self):  # неизвестная команда
        msg = str(self.repository.get_msg_text('not_understand').text)
        self.message.set_text(msg)
        self.message.set_tts(msg.replace('\n', '').replace('>', '').replace('<', ''))

    def help(self):  # вывод помощи
        msg = str(self.repository.get_msg_text('help').text)
        self.message.set_text(msg)
        self.message.set_tts(msg.replace('\\n', '').replace('>', '').replace('<', ''))
