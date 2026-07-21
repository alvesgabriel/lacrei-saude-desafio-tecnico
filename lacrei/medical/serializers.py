from rest_framework import serializers

from lacrei.medical import models


class ProfessionalSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Professional
        fields = [
            'id',
            'social_name',
            'profession',
            'email',
            'phone',
            'address',
            'user',
        ]
        extra_kwargs = {'user': {'write_only': True}}


class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    professional = ProfessionalSerializer(read_only=True)
    professional_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Professional.objects.all(),
        source='professional',
        write_only=True
    )

    class Meta:
        model = models.Appointment
        fields = ['id', 'date', 'professional', 'professional_id', 'user']
