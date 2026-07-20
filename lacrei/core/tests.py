import factory
import pytest
from rest_framework import status

from lacrei.core.models import CustomUser


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


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f'test{n}@test.com')
    password = 't3st#42'
    is_active = True


def test_create_user_status_code_201(client, db, user_dict):
    response = client.post(
        '/users/',
        data=user_dict,
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_user_body_response(client, db, user_dict):
    response = client.post(
        '/users/',
        data=user_dict,
    )
    expected = user_dict.copy()
    expected['id'] = 1
    del expected['password']
    assert response.json() == expected


def test_get_user_by_id_status_code_200(client, db, authorization):
    response = client.get(
        '/users/1/',
        headers=authorization,
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_user_by_id_unauthorazed_401(client, db, user_post):
    response = client.get('/users/1/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login(client, db, user_post):
    user_data = {
        'email': user_post['email'],
        'password': user_post['password'],
    }
    response = client.post('/api/token/', data=user_data)
    expected = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in expected
    assert 'refresh' in expected
