from .models import UserDetail
from django. http import JsonResponse
from .serializer import UserSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET','POST'])
def register_user(request):
    if request.method =='GET':
        user = UserDetail.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserDetail(data = request.data)
        if serializer.is_valid():
            serializer.referral_code =  f"D{generate_random_alphanumeric(2)}R{generate_random_alphanumeric(2)}"
            if serializer.referred_by:
                referred_user = UserDetail.objects.get(referral_code=serializer.referred_by)
                referred_user.referral_point += 10
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors) 

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def UserList(request):
    if request.method == 'GET':
        user = UserDetail.objects.all()
        serializer =UserSerializer(user, many = True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = UserDetail.objects.get(pk=pk)
    except  UserDetail.DoesNotExist:
        return Response(status=404)


    if request.method == 'GET':
        serializer = UserSerializer(user, safe = False)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def referr_detail(request):
    if request.mrthod =='GET':
        referr_user = request.user_detail.user.referr_code
        referring = UserDetail.objects.filter(referred_by = referr_user)
        if referring:
            serializer = UserSerializer(referring, safe=False)
            return Response(serializer)
        else: 
            serializer.UserSerializer(referr_user, safe=False)
            return Response(referr_user)
        


import random
import string

def generate_random_alphanumeric(length):
    """
    Generates a random alphanumeric string of the specified length.
    """
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



 



