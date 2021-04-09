class SessionStorage:
    def __init__(self):
        self.sessionStorage = {}

    def add_session(self, sessionId):
        if sessionId in self.sessionStorage.keys():
            return
        self.sessionStorage[sessionId] = {'wait_for_confirm': False}

    def is_wait_for_confirm(self, sessionId):
        if sessionId not in self.sessionStorage.keys():
            self.add_session(sessionId)
        return self.sessionStorage[sessionId]['wait_for_confirm']

    def set_confirm(self, sessionId, event):
        self.add_session(sessionId)
        self.sessionStorage[sessionId]['wait_for_confirm'] = True
        self.sessionStorage[sessionId]['event'] = event

    def delete_confirm(self, sessionId):
        self.add_session(sessionId)
        self.sessionStorage[sessionId]['wait_for_confirm'] = False
        try:
            del self.sessionStorage[sessionId]['event']
        finally:
            pass

    def get_confirm_event(self, sessionId):
        if self.is_wait_for_confirm(sessionId):
            return self.sessionStorage[sessionId]['event']
        return None

