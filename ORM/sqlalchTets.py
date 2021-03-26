from SqlalchemyOperator import SqlalchemyOperator
from data.events import Event
from data import db_session

repository = SqlalchemyOperator('db/schedule.db')
# repository.add_user(634554455644556)
user = repository.get_user(634554455644556)
print(user.id)
print(repository.user_is_created(634554451244556))  # False
print(repository.user_is_created(634554455644556))  # True
print(repository.get_users())
repository.delete_user(user)