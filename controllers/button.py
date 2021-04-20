class Button:
    """Кнопка для api алисы"""

    def __init__(self, title, url='', payload=None, hide=True):
        self.title = title  # текст кнопки
        self.url = url  # ссылка, которая откроется при нажатии
        # словарь, которые передатся навыку, если будет нажата кнопка
        self.payload = {} if payload is None else payload
        self.hide = hide  # True - появится на вводом текста, False - появится под сообщением и не пропадет

    def __iter__(self):
        #  ф-я нужна для вызова dict(), для отправки ответа к api, просто формирует итератор
        builded = {'title': self.title,
                   'hide': self.hide}
        if self.url:
            builded['url'] = self.url
        if self.payload:
            builded['payload'] = self.payload
        for key, value in builded.items():
            yield (key, value)
