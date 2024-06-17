import os
import pytest
import requests
import yaml
import random
import string
import base64

# BASE_URL = "http://146.190.145.51:8000"
BASE_URL = "http://localhost:8000"
POST_SIGNUP_PATH = "/signup"
GET_USER_PATH = "/users/"
UPDATE_USER_PATH = "/users/"
POST_CLOSE_PATH = "/close"

reserved_user = {
    "user_id": "TaroYamada",
    "password": "PaSSwd4TY"
}

def rand_str(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

user4test = {
    "user_id": "TestOP" + rand_str(6),
    "password": rand_str(16)
}

def print_response(response):
    # print(f"Status Code: {response.status_code}")
    # print(f"Response JSON: {response.json()}")
    print(f"{response}")

@pytest.fixture
def client():
    return requests.Session()

def test_cannot_create_account_without_user_id_and_password(client):
    response = client.post(BASE_URL + POST_SIGNUP_PATH, json={})
    print_response(response)
    assert response.status_code == 400
    assert response.json()['detail']['message'] == 'Account creation failed'
    assert 'required' in response.json()['detail']['cause']

def test_can_create_account(client):
    response = client.post(BASE_URL + POST_SIGNUP_PATH, json=user4test)
    assert response.status_code == 200
    assert response.json()['message'] == 'Account successfully created'

def test_cannot_get_user_information_without_authorization(client):
    response = client.get(BASE_URL + GET_USER_PATH + reserved_user['user_id'])
    print_response(response)
    assert response.status_code == 401
    assert response.json()['message'] == 'Authentication Failed'

def test_can_get_information_of_reserved_user_account(client):
    #print_response((BASE_URL + GET_USER_PATH + reserved_user['user_id'], reserved_user['user_id'], reserved_user['password']))
    response = client.get(BASE_URL + GET_USER_PATH + reserved_user['user_id'], auth=(reserved_user['user_id'], reserved_user['password']))
    print_response(response)
    assert response.status_code == 200
    assert response.json()['message'] == 'User details by user_id'

def test_can_get_user_information_of_different_user_id(client):
    response = client.get(BASE_URL + GET_USER_PATH + user4test['user_id'], auth=(reserved_user['user_id'], reserved_user['password']))
    assert response.status_code == 200
    assert response.json()['message'] == 'User details by user_id'

def test_cannot_update_user_information_without_authorization(client):
    user = {
        "nickname": "Nickname" + rand_str(8),
        "comment": "Comment" + rand_str(16)
    }
    response = client.patch(BASE_URL + UPDATE_USER_PATH + user4test['user_id'], json=user)
    assert response.status_code == 401
    assert response.json()['message'] == 'Authentication Failed'

def test_can_update_user_information(client):
    user = {
        "nickname": "Nickname" + rand_str(8),
        "comment": "Comment" + rand_str(16)
    }
    response = client.patch(BASE_URL + UPDATE_USER_PATH + user4test['user_id'], auth=(user4test['user_id'], user4test['password']), json=user)
    assert response.status_code == 200
    assert response.json()['message'] == 'User successfully updated'

def test_cannot_update_information_of_different_account(client):
    user = {
        "nickname": "Nickname" + rand_str(8),
        "comment": "Comment" + rand_str(16)
    }
    response = client.patch(BASE_URL + UPDATE_USER_PATH + reserved_user['user_id'], auth=(user4test['user_id'], user4test['password']), json=user)
    assert response.status_code == 403
    assert response.json()['message'] == 'No Permission for Update'

def test_cannot_delete_account_without_authorization(client):
    response = client.post(BASE_URL + POST_CLOSE_PATH)
    print_response(response)
    assert response.status_code == 401
    assert response.json()['message'] == 'Authentication Failed'

def test_can_delete_account(client):
    response = client.post(BASE_URL + POST_CLOSE_PATH, auth=(user4test['user_id'], user4test['password']))
    print_response(response)
    assert response.status_code == 200
    assert response.json()['message'] == 'Account and user successfully removed'
