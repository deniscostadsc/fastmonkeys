import pytest

from fastmonkeys import app
from fastmonkeys.database import Base, engine, init_db


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

    response = client.post('/register', data=data)
    assert response.status_code == 302


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
