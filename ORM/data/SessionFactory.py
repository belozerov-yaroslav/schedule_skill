import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

from ORM.data import __all_models

from ORM.data.events import Event


class SessionFactory:
    _instance = None
    SqlAlchemyBase = dec.declarative_base()

    @staticmethod
    def get_instance(db_file):
        if not SessionFactory._instance:
            SessionFactory._instance = SessionFactory(db_file)
        return SessionFactory._instance

    def __init__(self, db_file):
        self.global_init(db_file)

    def global_init(self, db_file):
        if not db_file or not db_file.strip():
            raise Exception("Необходимо указать файл базы данных.")

        conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
        print(f"Подключение к базе данных по адресу {conn_str}")

        engine = sa.create_engine(conn_str, echo=False)
        self.__factory = orm.sessionmaker(bind=engine)

        self.SqlAlchemyBase.metadata.create_all(engine)

    def create_session(self) -> Session:
        return self.__factory()


if __name__ == '__main__':
    test = SessionFactory.get_instance('ORM/db/schedule.db')
    db_sess = test.create_session()

    print(db_sess.query(Event).all())
    test1 = SessionFactory.get_instance('ORM/db/schedule.db')
    print(id(test1) == id(test))


