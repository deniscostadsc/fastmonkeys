from datetime import date

import pytest

from fastmonkeys.database import db_session, Base, engine, init_db
from fastmonkeys.forms import RegisterForm, LoginForm
from fastmonkeys.models import Monkey


@pytest.fixture(scope="function")
def start_database():
    Base.metadata.drop_all(bind=engine)
    init_db()


def test_registration_form_fail_validate_email(start_database):
    monkey = Monkey('Lemmy Kilmister', 'lemmy@mail.com', date.today(), '123456')
    db_session.add(monkey)
    db_session.commit()
    form = RegisterForm(
        name='Lemmy Kilmister',
        email='lemmy@mail.com',
        date_of_birth=date.today(),
        password='123456'
    )
    assert not form.validate()


def test_registration_form_validate_email(start_database):
    monkey = Monkey('Lemmy Kilmister', 'lemmy@mail.com', date.today(), '123456')
    db_session.add(monkey)
    db_session.commit()
    form = RegisterForm(
        name='Lemmy Kilmister',
        email='otheremail@mail.com',
        date_of_birth=date.today(),
        password='123456'
    )
    assert form.validate()


def test_login(start_database):
    monkey = Monkey('Lemmy Kilmister', 'lemmy@mail.com', date.today(), '123456')
    db_session.add(monkey)
    db_session.commit()
    form = LoginForm(email='lemmy@mail.com', password='123456')
    assert form.validate()
