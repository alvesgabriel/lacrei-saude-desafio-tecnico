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

    def create(self, validated_data):
        return super().create(validated_data)
