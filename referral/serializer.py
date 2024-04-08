from .models import UserDetail
from rest_framework import serializers
# from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ('first_name', 'email', 'password','referred_by','date_joined')      
    
        