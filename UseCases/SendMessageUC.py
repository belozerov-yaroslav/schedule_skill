from UseCases.UseCase import UseCase


class SendMessageUC(UseCase):
    def not_understand(self):
        self.message.set_text(self.repository.get_msg_text('not_understand').text)

    def help(self):
        self.message.set_text(self.repository.get_msg_text('help').text)
