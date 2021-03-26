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
    def add_user_event(self, user, date, text, periodicity=0, extra_text=''):
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
    def get_real_time(self, datetime):
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
