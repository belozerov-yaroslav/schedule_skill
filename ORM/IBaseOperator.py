from abc import ABC, abstractmethod


class IBaseOperator(ABC):
    @abstractmethod
    def __init__(self, repository_name):
        pass

    @abstractmethod
    def add_user(self, user_id):
        pass

    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def delete_user(self, user):
        pass

    @abstractmethod
    def delete_user_event(self, event):
        pass

    @abstractmethod
    def get_user_events(self, user):
        pass

    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def user_is_created(self, user_id):
        pass

    @abstractmethod
    def delete_useless_events(self):
        pass

    @abstractmethod
    def delete_old_users(self):
        pass

    @abstractmethod
    def update_user_info(self, user):
        pass

    @abstractmethod
    def add_event(self, event):
        pass

    @abstractmethod
    def get_event_description(self, event):
        pass

    @abstractmethod
    def get_msg_text(self, name):
        pass
