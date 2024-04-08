# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser



class UserDetail(AbstractUser):
    email = models.EmailField(unique=True)
    referral_code = models.CharField(max_length=20)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    referral_point = models.PositiveIntegerField(default=0)


# serializers.py





