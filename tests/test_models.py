from datetime import date

import pytest

from fastmonkeys.models import Monkey


@pytest.fixture(scope="module")
def monkey():
    return Monkey('Denis Costa', 'myemail@gmail.com', date.today(), '123456')


def test_hash_password(monkey):
    assert monkey.password != '123456'


def test_check_password(monkey):
    assert monkey.check_password('123456')


def test_is_authenticated(monkey):
    assert monkey.is_authenticated()


def test_is_active(monkey):
    assert monkey.is_active()


def test_is_anonymous(monkey):
    assert not monkey.is_anonymous()
