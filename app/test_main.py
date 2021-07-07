from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    assert client.get('/').status_code == 200


def test_login():
    request = client.post(
        '/auth/login', json={'username': 'user7', 'password': 'user7'})
    assert request.status_code == 200


def test_fail_login():
    request = client.post(
        '/auth/login', json={'username': 'user7', 'password': 'user8'})
    assert request.status_code == 400


def test_register():
    request = client.post(
        '/auth/register', json={'username': 'usr1',
                                'password': 'usr1',
                                'first_name': 'usr1',
                                'last_name': 'usr1',
                                'age': 0,
                                'email': 'usr1@example.com'}
    )
    assert request.status_code == 201


def test_fail_register():
    request = client.post(
        '/auth/register', json={'username': 'user7',
                                'password': 'user7',
                                'first_name': 'string',
                                'last_name': 'string',
                                'age': 0,
                                'email': 'string'}
    )
    assert request.status_code == 400


def test_get_appointment():
    assert client.get('/appointment').status_code == 200
