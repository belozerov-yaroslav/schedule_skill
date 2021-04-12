class Button:
    def __init__(self, title, url='', payload=None, hide=True):
        self.title = title
        self.url = url
        self.payload = {} if payload is None else payload
        self.hide = hide

    def __iter__(self):
        builded = {'title': self.title,
                   'hide': self.hide}
        if self.url:
            builded['url'] = self.url
        if self.payload:
            builded['payload'] = self.payload
        for key, value in builded.items():
            yield (key, value)

