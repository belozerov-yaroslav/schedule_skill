from data import db_session
from data.users import User
from data.events import Event
from data.event_descriptions import EventDescription


def main():
    db_session.global_init('db/schedule.db')
    session = db_session.create_session()

    user = User()
    user.id = 654984156316546
    session.add(user)
    session.commit()

    event = Event(periodcity=0,
                  user_id=654984156316546,
                  text='сходить в магазин')
    session.add(event)
    session.commit()

    event = Event(id=15,
                  periodcity=1,
                  user_id=654984156316546,
                  text='запустить робот пылесос')
    session.add(event)
    session.commit()

    event_description = EventDescription(event_id=15,
                                         text='2')
    session.add(event_description)
    session.commit()


if __name__ == '__main__':
    main()
