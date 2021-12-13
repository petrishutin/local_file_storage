import os

import pytest

from requests.auth import HTTPBasicAuth
from fastapi.testclient import TestClient

from app.main import app
from app.settings import config


@pytest.fixture(scope='session')
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='session')
def basic_auth():
    return HTTPBasicAuth(config.STORAGE_USER, config.PASSWORD)


@pytest.fixture(scope='module')
def txt_file():
    with open(f"{config.BASE_DIR}/../tests/test.txt", "rb") as txt_file:
        yield txt_file


@pytest.fixture(scope='module')
def odt_file():
    with open(f"{config.BASE_DIR}/../tests/test.odt", "rb") as odt_file:
        yield odt_file


@pytest.fixture(scope='module')
def new_file_hash():
    return {}


def test_upload_201(client, basic_auth, txt_file, new_file_hash):
    response = client.post('/upload', auth=basic_auth, files={'uploaded_file': txt_file})
    assert response.status_code == 201, response.text
    file_hash = response.text
    assert file_hash
    new_file_hash['file_hash'] = file_hash.replace('"', '')


def test_download_200(client, basic_auth, txt_file, new_file_hash):
    response = client.get(f"/download/{new_file_hash['file_hash']}", auth=basic_auth)
    assert response.status_code == 200, response.text
    txt_file.seek(0)
    assert txt_file.read() == response.content


def test_update_200(client, basic_auth, odt_file, new_file_hash):
    response = client.put(
        f"/update/",
        auth=basic_auth,
        files={'uploaded_file': odt_file},
        data={'file_hash': new_file_hash['file_hash']}
    )
    assert response.status_code == 200, response.text
    assert response.text.replace('"', '') == f"file {new_file_hash['file_hash']} successfully updated"


def test_file_is_updated(client, basic_auth, odt_file, new_file_hash):
    response = client.get(f"/download/{new_file_hash['file_hash']}", auth=basic_auth)
    assert response.status_code == 200, response.text
    odt_file.seek(0)
    assert odt_file.read() == response.content


def test_delete_200(client, basic_auth, new_file_hash):
    response = client.delete(f"/delete/{new_file_hash['file_hash']}", auth=basic_auth)
    assert response.status_code == 200, response.text
    assert response.text.replace('"', '') == f"file {new_file_hash['file_hash']} successfully deleted"


def test_deleted_file_not_found_404(client, basic_auth, new_file_hash):
    response = client.get(f"/download/{new_file_hash['file_hash']}", auth=basic_auth)
    assert response.status_code == 404, response.text
    assert response.json()['detail'] == f"file {new_file_hash['file_hash']} not found", response.text
