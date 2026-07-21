import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client_api():
    return APIClient()


@pytest.fixture
def client_authorized(db, authorization):
    return APIClient(format='json', headers=authorization)


@pytest.fixture
def user_dict():
    return {
        'email': 'alice@example.com',
        'password': '4l1c342',
    }


@pytest.fixture
def user_post(client, user_dict):
    response = client.post(
        '/users/',
        data=user_dict,
    )
    user = response.json()
    user['password'] = user_dict['password']
    return user


@pytest.fixture
def token(client, user_post):
    response = client.post(
        '/api/token/',
        {
            'email': user_post['email'],
            'password': user_post['password'],
        },
    )
    return response.json()


@pytest.fixture
def authorization(client, token):
    return {'Authorization': f'Bearer {token["access"]}'}
