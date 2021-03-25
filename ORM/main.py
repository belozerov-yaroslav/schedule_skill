from data import db_session
from data.users import User
from data.events import Event
from data.event_descriptions import EventDescription


def main():
    db_session.global_init('db/schedule.db')
    session = db_session.create_session()


if __name__ == '__main__':
    main()