import factory
import pytest
from rest_framework import status

from lacrei.core.models import CustomUser
from lacrei.medical.models import Professional
from lacrei.medical.serializers import ProfessionalSerializer


@pytest.fixture
def professional_dict():
    return {
        'social_name': 'Alice',
        'profession': 'Medica',
        'address': 'Rua das Flores, 120',
        'email': 'alice@example.com',
        'phone': '+5521987654321',
    }


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f'test{n}@example.com')
    password = factory.Faker('pystr', min_chars=8, max_chars=8)


class ProfessionalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Professional

    profession = 'Médica'
    email = factory.Sequence(lambda n: f'test{n}@example.com')
    user_id = 1


def test_create_professional_status_code_201(
    client_api, db, professional_dict, authorization
):
    response = client_api.post(
        '/professionals/',
        headers=authorization,
        data=professional_dict,
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_professional_body_response(
    client_api, db, professional_dict, authorization
):
    response = client_api.post(
        '/professionals/',
        headers=authorization,
        data=professional_dict,
    )
    expected = professional_dict.copy()
    expected['id'] = 1
    assert response.json() == expected


def test_create_professional_error_unauthorazed_401(
    client_api, db, professional_dict
):
    response = client_api.post(
        '/professionals/',
        data=professional_dict,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_professional_get_by_id_status_code_200(
    client_api, db, authorization
):
    professional = ProfessionalFactory()
    response = client_api.get(
        f'/professionals/{professional.id}/',
        headers=authorization,
    )
    assert response.status_code == status.HTTP_200_OK


def test_create_professional_get_by_id_body_response(
    client_api, db, authorization
):
    professional = ProfessionalFactory()
    response = client_api.get(
        f'/professionals/{professional.id}/',
        headers=authorization,
    )
    expected = dict(ProfessionalSerializer(professional).data)
    assert response.json() == expected


def test_update_professional_by_id(
    client_authorized, db, professional_dict, authorization
):
    professional = ProfessionalFactory()
    response = client_authorized.put(
        f'/professionals/{professional.id}/',
        data=professional_dict,
    )
    expected = professional_dict.copy()
    expected['id'] = professional.id
    assert response.json() == expected


def test_update_professional_error_to_other_user(
    client_authorized, db, professional_dict, authorization
):
    user = UserFactory()
    professional = ProfessionalFactory(user_id=user.id)
    response = client_authorized.put(
        f'/professionals/{professional.id}/',
        data=professional_dict,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
