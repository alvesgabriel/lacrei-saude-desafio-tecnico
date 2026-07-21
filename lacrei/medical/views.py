from rest_framework import permissions, viewsets

from lacrei.medical import models, serializers
from lacrei.medical.permissions import IsOwner


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = models.Professional.objects.all()
    serializer_class = serializers.ProfessionalSerializer
    permission_classes = [IsOwner & permissions.IsAuthenticated]
