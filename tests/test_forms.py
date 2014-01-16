from datetime import date

from fastmonkeys.database import db_session, init_db
from fastmonkeys.forms import RegisterForm
from fastmonkeys.models import Monkey

init_db()


def test_fail_validate_email():
    monkey = Monkey('Denis Costa', 'myemail@mail.com', date.today(), '123456')
    db_session.add(monkey)
    db_session.commit()
    form = RegisterForm(
        name='Denis Costa',
        email='myemail@mail.com',
        date_of_birth=date.today(),
        password='123456'
    )
    assert not form.validate()


def test_validate_email():
    monkey = Monkey('Ramon One', 'ramone@mail.com', date.today(), '123456')
    db_session.add(monkey)
    db_session.commit()
    form = RegisterForm(
        name='Ramon One',
        email='otheremail@mail.com',
        date_of_birth=date.today(),
        password='123456'
    )
    assert form.validate()
