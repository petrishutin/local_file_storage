import pytest

from requests.auth import HTTPBasicAuth
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def new_user():
    return {'username': 'test1', 'password1': 'test', 'password2': 'test'}


def test_auth_get_200(client):
    response = client.get('/get_users', auth=HTTPBasicAuth('admin', 'admin'))
    assert response.status_code == 200


def test_add_user_201(client, new_user):
    response = client.post('/add_user', auth=HTTPBasicAuth('admin', 'admin'), json=new_user)
    assert response.status_code == 201


def test_new_user_operational(client, new_user):
    response = client.get('/get_users', auth=HTTPBasicAuth(new_user['username'], new_user['password1']))
    assert response.status_code == 200
    assert new_user['username'] in response.json()
