from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from lacrei.core.models import CustomUser


class Professional(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    social_name = models.CharField(max_length=128, blank=False, null=False)
    profession = models.CharField(max_length=64, blank=False, null=False)
    email = models.EmailField(max_length=255, unique=True)
    phone = PhoneNumberField()
    address = models.CharField(max_length=512, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Appointment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(verbose_name='appointment date')
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
