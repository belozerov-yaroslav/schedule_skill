# from SqlalchemyOperator import SqlalchemyOperator
from data.events import Event
from data.users import User
from data import db_session

# repository = SqlalchemyOperator('db/schedule.db')
# repository.add_user(634554455644556)
# user = repository.get_user(634554455644556)
# print(user.id)
# print(repository.user_is_created(634554451244556))  # False
# print(repository.user_is_created(634554455644556))  # True
# print(repository.get_users())
# repository.delete_user(user)
db_session.global_init('db/schedule.db')
db_sess = db_session.create_session()
event = Event(text='test', periodicity=0, user=db_sess.query(User).one())
db_sess.add(event)
db_sess.commit()
print(event.id)