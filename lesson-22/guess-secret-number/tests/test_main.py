import os
import pytest
from main import app
from models import User
from tinydb import TinyDB


@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["TESTING"] = "1"  # this creates a TinyDB test database. Works ONLY with smartninja-nosql on localhost!
    client = app.test_client()
    yield client

    cleanup()  # clean up after every test


def cleanup():
    # clean up the DB
    db = TinyDB('test_db.json')
    db.purge_tables()


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


def test_profile_edit(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    # GET
    response = client.get('/profile/edit')
    assert b'Edit your profile' in response.data

    # POST
    response = client.post('/profile/edit', data={"profile-name": "Test User 2", "profile-email": "test2@user.com"},
                           follow_redirects=True)
    assert b'Test User 2' in response.data
    assert b'test2@user.com' in response.data


def test_profile_delete(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    # GET
    response = client.get('/profile/delete')
    assert b'Delete your profile' in response.data

    # POST
    response = client.post('/profile/delete', follow_redirects=True)
    assert b'Enter your name' in response.data  # redirected back to the index site


def test_all_users(client):
    response = client.get('/users')
    assert b'<h3>Users</h3>' in response.data

    # create a new user
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get('/users')
    assert b'<h3>Users</h3>' in response.data
    assert b'Test User' in response.data


def test_user_details(client):
    # create a new user
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    # get user object from the database
    user = User.fetch_one(query=["email", "==", "test@user.com"])

    response = client.get('/user/{}'.format(user.id))
    assert b'test@user.com' in response.data
    assert b'Test User' in response.data
