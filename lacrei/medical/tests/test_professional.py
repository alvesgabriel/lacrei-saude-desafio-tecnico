import factory
import pytest
from rest_framework import status

from lacrei.core.tests import UserFactory
from lacrei.medical.models import Professional
from lacrei.medical.serializers import ProfessionalSerializer


class ProfessionalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Professional

    profession = 'Médica'
    email = factory.Sequence(lambda n: f'test{n}@example.com')
    user_id = 1


@pytest.fixture
def professional_dict():
    return {
        'social_name': 'Alice',
        'profession': 'Medica',
        'address': 'Rua das Flores, 120',
        'email': 'alice@example.com',
        'phone': '+5521987654321',
    }


def test_create_professional_status_code_201(
    client_authorized, db, professional_dict
):
    response = client_authorized.post(
        '/api/professionals/',
        data=professional_dict,
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_professional_body_response(
    client_authorized, db, professional_dict
):
    response = client_authorized.post(
        '/api/professionals/',
        data=professional_dict,
    )
    expected = professional_dict.copy()
    expected['id'] = 1
    expected['user_id'] = 1
    assert response.json() == expected


def test_create_professional_error_unauthorazed_401(
    client_api, db, professional_dict
):
    response = client_api.post(
        '/api/professionals/',
        data=professional_dict,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_professional_by_id_status_code_200(client_authorized, db):
    professional = ProfessionalFactory()
    response = client_authorized.get(
        f'/api/professionals/{professional.id}/',
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_professional_by_id_body_response(client_authorized, db):
    professional = ProfessionalFactory()
    response = client_authorized.get(
        f'/api/professionals/{professional.id}/',
    )
    expected = dict(ProfessionalSerializer(professional).data)
    assert response.json() == expected


def test_update_professional_by_id(client_authorized, db, professional_dict):
    professional = ProfessionalFactory()
    response = client_authorized.put(
        f'/api/professionals/{professional.id}/',
        data=professional_dict,
    )
    expected = professional_dict.copy()
    expected['id'] = professional.id
    expected['user_id'] = professional.user_id
    assert response.json() == expected


def test_update_professional_error_to_other_user(
    client_authorized, db, professional_dict
):
    user = UserFactory()
    professional = ProfessionalFactory(user_id=user.id)
    response = client_authorized.put(
        f'/api/professionals/{professional.id}/',
        data=professional_dict,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_professionals_filter_by_user_id(client_authorized, db):
    user = UserFactory()
    ProfessionalFactory.create_batch(7)
    ProfessionalFactory.create_batch(
        3,
        user_id=user.id,
    )
    response = client_authorized.get(
        f'/api/professionals/?user_id={user.id}',
    )
    expected = response.json()
    expected_count = 3
    assert expected.get('count') == expected_count


def test_list_professionals_filter_by_social_name(
    client_authorized,
    db,
):
    ProfessionalFactory.create_batch(7)
    ProfessionalFactory(
        social_name='Chapeleiro Maluco',
        profession='Psicologo',
    )
    response = client_authorized.get(
        '/api/professionals/?social_name=chapeleiro',
    )
    expected = response.json()
    expected_count = 1
    assert expected.get('count') == expected_count


def test_list_professionals_filter_by_profession(
    client_authorized,
    db,
):
    ProfessionalFactory.create_batch(7)
    ProfessionalFactory(
        social_name='Chapeleiro Maluco',
        profession='Psicologo',
    )
    ProfessionalFactory(
        social_name='Alice',
        profession='Psiquiatra',
    )
    response = client_authorized.get(
        '/api/professionals/?profession=psi',
    )
    expected = response.json()
    expected_count = 2
    assert expected.get('count') == expected_count
