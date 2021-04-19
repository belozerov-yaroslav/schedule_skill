class SessionStorage:
    def __init__(self):
        self.sessionStorage = {}

    def add_session(self, session_id):
        if session_id in self.sessionStorage.keys():
            return
        self.sessionStorage[session_id] = {'wait_for_confirm': False,
                                           'wait_for_delete': False,
                                           'delete_events': []}

    def is_wait_for_confirm(self, session_id):
        self.add_session(session_id)
        return self.sessionStorage[session_id]['wait_for_confirm']

    def set_confirm(self, session_id, event):
        self.add_session(session_id)
        self.sessionStorage[session_id]['wait_for_confirm'] = True
        self.sessionStorage[session_id]['event'] = event

    def delete_confirm(self, session_id):
        self.add_session(session_id)
        self.sessionStorage[session_id]['wait_for_confirm'] = False
        try:
            del self.sessionStorage[session_id]['event']
        finally:
            pass

    def get_confirm_event(self, session_id):
        if self.is_wait_for_confirm(session_id):
            return self.sessionStorage[session_id]['event']
        return None

    def set_delete(self, session_id, delete_events):
        self.add_session(session_id)
        self.sessionStorage[session_id]['wait_for_delete'] = True
        self.sessionStorage[session_id]['delete_events'] = delete_events

    def is_wait_for_delete(self, session_id):
        self.add_session(session_id)
        return self.sessionStorage[session_id]['wait_for_delete']

    def delete_events(self, session_id):
        self.add_session(session_id)
        return self.sessionStorage[session_id]['delete_events']

    def delete_wait_delete(self, session_id):
        self.add_session(session_id)
        self.sessionStorage[session_id]['wait_for_delete'] = False
        self.sessionStorage[session_id]['delete_events'] = []
