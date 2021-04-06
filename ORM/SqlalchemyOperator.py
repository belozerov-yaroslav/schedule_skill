from .IBaseOperator import IBaseOperator
from .data import db_session
from .data.users import User
from .data.events import Event
from .data.event_descriptions import EventDescription
import datetime


def open_db_sess(func):

    def decorated(*args, **kwargs):
        db_sess = db_session.create_session()
        res = func(*args, db_sess=db_sess, **kwargs)
        db_sess.close()
        return res
    return decorated


def open_and_commit_db_sess(func):

    def decorated(*args, **kwargs):
        db_sess = db_session.create_session()
        res = func(*args, db_sess=db_sess, **kwargs)
        db_sess.commit()
        db_sess.close()
        return res

    return decorated


class SqlalchemyOperator(IBaseOperator):
    def __init__(self, repository_name):
        db_session.global_init(repository_name)

    @open_and_commit_db_sess
    def add_user(self, user_id, db_sess=None):
        db_sess.add(User(yandex_id=user_id))

    @open_db_sess
    def get_user(self, yandex_id, db_sess=None):
        user = db_sess.query(User).filter(User.yandex_id == yandex_id).one()
        return user

    @open_and_commit_db_sess
    def delete_user(self, user, db_sess=None):
        db_sess.delete(user)

    @open_and_commit_db_sess
    def delete_user_event(self, event, db_sess=None):
        db_sess.delete(event)

    @open_db_sess
    def get_user_events(self, user, db_sess=None):
        events = db_sess.query(Event).filter(Event.user == user).all()
        return events

    @open_db_sess
    def get_users(self, db_sess=None):
        users = db_sess.create_session().query(User).all()
        return users

    @open_db_sess
    def user_is_created(self, yandex_id, db_sess=None):
        return bool(len(db_sess.query(User).filter(User.yandex_id == yandex_id).all()))

    def delete_useless_events(self):
        pass

    def delete_old_users(self):
        pass

    @open_and_commit_db_sess
    def update_user_info(self, user: User, db_sess=None):
        user.last_visit = datetime.datetime.now()
        user.num_of_vis += 1
        db_sess.add(user)

    @open_and_commit_db_sess
    def add_event(self, event, event_description=None, db_sess=None):
        db_sess.add(event)
        if not event_description is None:
            event_description.event = event
            db_sess.add(event_description)

    @open_db_sess
    def get_event_description(self, event, db_sess=None):
        event_description = db_sess.query(EventDescription).filter(EventDescription.event == event).one()
        return event_description
