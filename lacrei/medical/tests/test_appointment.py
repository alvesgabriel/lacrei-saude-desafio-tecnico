from datetime import datetime

import factory
import pytest
from rest_framework import status

from lacrei.medical.models import Appointment, Professional
from lacrei.medical.serializers import ProfessionalSerializer, AppointmentSerializer
from lacrei.medical.tests.test_professional import ProfessionalFactory, UserFactory


class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appointment

    date = datetime(2026, 1, 1, 16, 20)
    professional = factory.SubFactory(ProfessionalFactory)
    user_id = 1


@pytest.fixture
def appointment_dict(user_post):
    professional = ProfessionalFactory()
    return {
        'date': '2026-01-01T16:20:00Z',
        'professional_id': professional.id,
    }


def test_create_appointment_status_code_201(
    client_authorized, db, appointment_dict
):
    response = client_authorized.post(
        '/appointments/',
        data=appointment_dict,
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_appointment_body_response(
    client_authorized, db, appointment_dict
):
    professional = dict(
        ProfessionalSerializer(
            Professional.objects.get(id=appointment_dict['professional_id'])
        ).data
    )
    response = client_authorized.post(
        '/appointments/',
        data=appointment_dict,
    )
    expected = {
        'id': 1,
        'date': appointment_dict['date'],
        'professional': professional,
    }
    assert response.json() == expected


def test_create_appointment_error_unauthorazed_401(
    client_api, db, appointment_dict
):
    response = client_api.post(
        '/appointments/',
        data=appointment_dict,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_appointment_by_id_status_code_200(    client_authorized, db):
    appointment = AppointmentFactory()
    response = client_authorized.get(
        f'/appointments/{appointment.id}/',
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_appointment_by_id_body_response(
    client_authorized, db,
):
    appointment = AppointmentFactory()
    response = client_authorized.get(
        f'/appointments/{appointment.id}/',
    )
    expected = dict(AppointmentSerializer(appointment).data)
    assert response.json() == expected


def test_update_appointment_by_id(
    client_authorized, db, appointment_dict
):
    appointment = AppointmentFactory()
    response = client_authorized.put(
        f'/appointments/{appointment.id}/',
        data=appointment_dict,
    )
    appointment.refresh_from_db()
    expected = dict(AppointmentSerializer(appointment).data)
    assert response.json() == expected


def test_update_appointment_error_to_other_user(
    client_authorized, db, appointment_dict
):
    user = UserFactory()
    appointment = AppointmentFactory(user_id=user.id)
    response = client_authorized.put(
        f'/appointments/{appointment.id}/',
        data=appointment_dict,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_appointment_by_id(
    client_authorized, db
):
    appointment = AppointmentFactory()
    response = client_authorized.delete(
        f'/appointments/{appointment.id}/',
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_appointment_by_error(
    client_authorized, db
):
    user = UserFactory()
    appointment = AppointmentFactory(user_id=user.id)
    response = client_authorized.delete(
        f'/appointments/{appointment.id}/',
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
