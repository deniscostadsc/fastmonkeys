from datetime import date

import mock
import pytest

from fastmonkeys.models import Monkey
from fastmonkeys.database import db_session, engine, init_db, Base
from fastmonkeys import load_user


@pytest.fixture(scope="module")
def monkey():
    return Monkey('Denis Costa', 'myemail@gmail.com', date.today(), '123456')


@pytest.fixture(scope="function")
def start_database():
    Base.metadata.drop_all(bind=engine)
    init_db()


def test_hash_password(monkey):
    assert monkey.password != '123456'


def test_check_password(monkey):
    assert monkey.check_password('123456')


@mock.patch('fastmonkeys.models.today')
def test_calculate_age_in_the_begining_of_the_year(today):
    today.return_value = date(2014, 1, 1)
    monkey = Monkey('Denis Costa', 'myemail@gmail.com', date(1987, 7, 17), '123456')
    assert monkey.age == 26


@mock.patch('fastmonkeys.models.today')
def test_calculate_age_in_your_birthday(today):
    today.return_value = date(2014, 7, 17)
    monkey = Monkey('Denis Costa', 'myemail@gmail.com', date(1987, 7, 17), '123456')
    assert monkey.age == 27


@mock.patch('fastmonkeys.models.today')
def test_calculate_age_in_the_end_of_the_year(today):
    today.return_value = date(2014, 12, 31)
    monkey = Monkey('Denis Costa', 'myemail@gmail.com', date(1987, 7, 17), '123456')
    assert monkey.age == 27


def test_is_authenticated(monkey):
    assert monkey.is_authenticated()


def test_is_active(monkey):
    assert monkey.is_active()


def test_is_anonymous(monkey):
    assert not monkey.is_anonymous()


def test_get_id(monkey):
    db_session.add(monkey)
    db_session.commit()
    assert monkey.get_id()


def test_repr(monkey):
    my_monkey = eval(monkey.__repr__())
    assert my_monkey.name == monkey.name


def test_load_user(monkey):
    db_session.add(monkey)
    db_session.commit()
    assert isinstance(load_user(monkey.get_id()), Monkey)
    assert load_user(monkey.get_id()).name == monkey.name


def test_fail_load_user(monkey, start_database):
    assert load_user(u'1') is None
