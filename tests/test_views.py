import pytest

from fastmonkeys import app


@pytest.fixture(scope="module")
def client():
    return app.test_client()


def test_index_status_code(client):
    response = client.get('/')
    assert response.status_code == 200


def test_register_status_code(client):
    response = client.get('/register')
    assert response.status_code == 200


def test_register(client):
    data = {
        'name': 'Lemmy Kilmister',
        'email': 'lemmy@mail.com',
        'date_of_birth': '09/12/1954',
        'password': '123456'
    }
    response = client.post('/register', data=data)
    assert response.status_code == 302
