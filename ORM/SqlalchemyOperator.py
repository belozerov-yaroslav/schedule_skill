from .IBaseOperator import IBaseOperator
from .data import db_session
from .data.users import User
from .data.events import Event
from .data.event_descriptions import EventDescription
import datetime


def decorate_test(func):

    def decorated(*args, **kwargs):
        db_sess = db_session.create_session()
        res = func(*args, db_sess=db_sess, **kwargs)
        db_sess.close()
        return res

    return decorated


class SqlalchemyOperator(IBaseOperator):
    def __init__(self, repository_name):
        db_session.global_init(repository_name)

    def test(self, func):
        pass

    def add_user(self, user_id):
        db_sess = db_session.create_session()
        db_sess.add(User(yandex_id=user_id))
        db_sess.commit()
        db_sess.close()

    @decorate_test
    def get_user(self, yandex_id, db_sess=None):
        user = db_sess.query(User).filter(User.yandex_id == yandex_id).one()
        return user

    def delete_user(self, user):
        db_sess = db_session.create_session()
        db_sess.delete(user)
        db_sess.commit()
        db_sess.close()

    def add_user_event(self, user, date, text, periodicity=0, extra_text=''):
        pass

    def delete_user_event(self, event):
        db_sess = db_session.create_session()
        db_sess.delete(event)
        db_sess.commit()
        db_sess.close()

    def get_user_events(self, user):
        db_sess = db_session.create_session()
        events = db_sess.query(Event).filter(Event.user == user).all()
        db_sess.close()
        return events

    def get_users(self):
        users = db_session.create_session().query(User).all()
        return users

    def user_is_created(self, yandex_id):
        db_sess = db_session.create_session()
        if len(db_sess.query(User).filter(User.yandex_id == yandex_id).all()):
            db_sess.close()
            return True
        db_sess.close()
        return False

    def get_real_time(self, datetime):
        pass

    def delete_useless_events(self):
        pass

    def delete_old_users(self):
        pass

    def update_user_info(self, user: User):
        db_sess = db_session.create_session()
        user.last_visit = datetime.datetime.now()
        user.num_of_vis += 1
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()

    def add_event(self, event, event_description=None):
        db_sess = db_session.create_session()
        db_sess.add(event)
        if not event_description is None:
            event_description.event = event
            db_sess.add(event_description)
            print(event_description)
        db_sess.commit()
        db_sess.close()

    def get_event_description(self, event):
        db_sess = db_session.create_session()
        event_description = db_sess.query(EventDescription).filter(EventDescription.event == event).one()
        db_sess.close()
        return event_description
