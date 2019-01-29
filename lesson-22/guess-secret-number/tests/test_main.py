import os
import pytest
from main import app
from models import User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["TESTING"] = "1"  # this creates a TinyDB test database. Works ONLY with smartninja-odm on localhost!
    client = app.test_client()
    yield client


def test_index_not_logged_in(client):
    response = client.get('/')
    assert b'Enter your name' in response.data


def test_index_logged_in(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get('/')
    assert b'Enter your guess' in response.data


def test_result_correct(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    user = User.fetch_one(query=["email", "==", "test@user.com"])  # get user object from the database
    User.edit(obj_id=user.id, secret_number=22)  # change the secret number to 22

    response = client.post('/result', data={"guess": 22})  # enter the correct guess
    assert b'Correct! The secret number is 22' in response.data


def test_result_incorrect_try_bigger(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    user = User.fetch_one(query=["email", "==", "test@user.com"])
    User.edit(obj_id=user.id, secret_number=22)

    response = client.post('/result', data={"guess": 13})  # enter the wrong guess (too small)
    assert b'Your guess is not correct... try something bigger.' in response.data


def test_result_incorrect_try_smaller(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    user = User.fetch_one(query=["email", "==", "test@user.com"])
    User.edit(obj_id=user.id, secret_number=22)

    response = client.post('/result', data={"guess": 27})  # enter the wrong guess (too big)
    assert b'Your guess is not correct... try something smaller.' in response.data


def test_profile(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get('/profile')
    assert b'Your profile' in response.data
