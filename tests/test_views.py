from datetime import date

import pytest

from fastmonkeys import app
from fastmonkeys.database import Base, engine, init_db, db_session
from fastmonkeys.models import Monkey


@pytest.fixture(scope="function")
def start_database():
    Base.metadata.drop_all(bind=engine)
    init_db()


@pytest.fixture(scope="module")
def client():
    return app.test_client()


def test_login_status_code(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login(client, start_database):
    monkey = Monkey('Lemmy Kilmister', 'lemmy@mail.com', date.today(), '123456')
    db_session.add(monkey)
    db_session.commit()

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    response = client.post('/', data=data)
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

    client.post('/register', data=data)

    data = {
        'email': 'lemmy@mail.com',
        'password': '123456'
    }

    client.post('/', data=data)

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

    response = client.post('/register', data=data)
    assert response.status_code == 302
