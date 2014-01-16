from datetime import date

from fastmonkeys.models import Monkey


def test_hash_password():
    monkey = Monkey('Denis Costa', 'myemail@gmail.com', date.today(), '123456')
    assert monkey.password != '123456'


def test_check_password():
    monkey = Monkey('Denis Costa', 'myemail@gmail.com', date.today(), '123456')
    assert monkey.check_password('123456')


def test_is_authenticated():
    monkey = Monkey('Denis Costa', 'myemail@gmail.com', date.today(), '123456')
    assert monkey.is_authenticated()


def test_is_active():
    monkey = Monkey('Denis Costa', 'myemail@gmail.com', date.today(), '123456')
    assert monkey.is_active()


def test_is_anonymous():
    monkey = Monkey('Denis Costa', 'myemail@gmail.com', date.today(), '123456')
    assert not monkey.is_anonymous()
