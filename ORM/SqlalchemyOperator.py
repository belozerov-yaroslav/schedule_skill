from .IBaseOperator import IBaseOperator
from .data import db_session
from .data.users import User
import datetime


class SqlalchemyOperator(IBaseOperator):
    def __init__(self, repository_name):
        db_session.global_init(repository_name)

    def add_user(self, user_id):
        db_sess = db_session.create_session()
        db_sess.add(User(yandex_id=user_id))
        db_sess.commit()
        db_sess.close()

    def get_user(self, yandex_id):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.yandex_id == yandex_id).one()
        db_sess.close()
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
        pass

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
