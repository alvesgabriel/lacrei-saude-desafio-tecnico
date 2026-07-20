import typing

from rest_framework import serializers

from lacrei.core import models


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    @typing.override
    def create(self, validated_data):
        user = models.CustomUser.objects.create_user(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
