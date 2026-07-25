from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from lacrei.medical import models, serializers
from lacrei.medical.permissions import IsOwner


class ProfessionalFilter(filters.FilterSet):
    social_name = filters.CharFilter(
        field_name='social_name', lookup_expr='icontains'
    )
    profession = filters.CharFilter(
        field_name='profession', lookup_expr='icontains'
    )
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    phone = filters.CharFilter(field_name='phone', lookup_expr='icontains')
    address = filters.CharFilter(field_name='address', lookup_expr='icontains')

    class Meta:
        model = models.Professional
        fields = [
            'social_name',
            'profession',
            'email',
            'phone',
            'address',
            'user_id',
        ]


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = models.Professional.objects.all().order_by('id')
    serializer_class = serializers.ProfessionalSerializer
    permission_classes = [IsOwner & permissions.IsAuthenticated]
    filterset_class = ProfessionalFilter


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = models.Appointment.objects.all().order_by('id')
    serializer_class = serializers.AppointmentSerializer
    permission_classes = [IsOwner & permissions.IsAuthenticated]
    filterset_fields = ('professional_id', 'user_id')
