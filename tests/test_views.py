import sys

import pytest

from fastmonkeys import app
from fastmonkeys.database import Base, engine, init_db
from fastmonkeys.models import Monkey


@pytest.fixture(scope="function")
def start_database():
    Base.metadata.drop_all(bind=engine)
    init_db()


@pytest.fixture(scope="function")
def client():
    return app.test_client()


def test_login_status_code(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    response = client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    assert not 'Set-Cookie' in response.headers

    response = client.post('/', data=data)
    assert 'Set-Cookie' in response.headers
    assert response.status_code == 302


def test_fail_login(client, start_database):
    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    response = client.post('/', data=data)
    assert response.status_code == 200


def test_logout(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    response = client.post('/register', data=data)
    assert not 'Set-Cookie' in response.headers

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    response = client.post('/', data=data)
    assert 'Set-Cookie' in response.headers

    response = client.get('/logout')
    assert response.status_code == 302


def test_fail_logout(client, start_database):
    response = client.get('/logout')
    assert response.status_code == 401


def test_register_status_code(client):
    response = client.get('/register')
    assert response.status_code == 200


def test_register(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    assert Monkey.query.filter(Monkey.email == 'lemmy@mail.com').count() == 0

    response = client.post('/register', data=data)
    assert response.status_code == 302
    assert Monkey.query.filter(Monkey.email == 'lemmy@mail.com').count() == 1


def test_view_profile(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)
    response = client.get('/monkeys/1/')
    assert response.status_code == 200


def test_fail_view_profile(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)
    response = client.get('/monkeys/9876543210/')
    assert response.status_code == 404


def test_edit_profile_status_code(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)

    response = client.get('/edit/')
    assert response.status_code == 200


def test_edit_email_profile(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)

    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy.kilmister@mail.com',
        'date_of_birth': '09/12/1954',
        'password': ''
    }

    response = client.post('/edit/', data=data)
    assert response.status_code == 200


def test_edit_password_profile(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)

    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456789'
    }

    response = client.post('/edit/', data=data)
    assert response.status_code == 200

    client.get('/logout/')

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456789'
    }

    response = client.post('/', data=data)

    assert 'Set-Cookie' in response.headers
    assert response.status_code == 302


def test_delete_monkey(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)
    assert Monkey.query.filter(Monkey.email == 'lemmy@mail.com').count() == 1

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)

    response = client.get('/delete/')
    assert response.status_code == 302
    assert Monkey.query.filter(Monkey.email == 'lemmy@mail.com').count() == 0


def test_list_monkeys(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)

    response = client.get('/monkeys/')
    assert response.status_code == 200

    if sys.version_info[0] == 3:
        assert bytearray('Lemmy Kilmister', 'utf-8') in response.data
    else:
        assert 'Lemmy Kilmister' in response.data


def test_fail_list_monkeys_bad_query_string(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)

    response = client.get('/monkeys/?page=a')
    assert response.status_code == 200


def test_list_monkeys_invalid_number(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)

    response = client.get('/monkeys/?page=123456')
    assert response.status_code == 404


def test_add_monkey_as_friend(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'name': 'Tom Araya',
        'email': 'Tom@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)

    response = client.get('/friend/2/')
    assert response.status_code == 302

    lemmy = Monkey.query.get(1)
    assert len(lemmy.friends) == 1


def test_unfriend(client, start_database):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'name': 'Tom Araya',
        'email': 'Tom@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)

    lemmy = Monkey.query.get(1)
    assert len(lemmy.friends) == 0

    response = client.get('/friend/2/')
    assert response.status_code == 302
    assert len(lemmy.friends) == 1

    response = client.get('/unfriend/2/')
    assert response.status_code == 302
    assert len(lemmy.friends) == 0
