import os
import pytest

# important: this line needs to be set BEFORE the "app" import
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from main import app, db


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    db.create_all()

    yield client


def cleanup():
    # clean up the DB (drop all tables)
    db.drop_all()


def test_index_not_logged_in(client):
    response = client.get('/')
    assert b'Enter your name' in response.data
    assert response.status_code == 200  # 200 means success. See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


def test_index_logged_in(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get('/')
    assert b'Enter your guess' in response.data
    # assert response.status_code == 200
