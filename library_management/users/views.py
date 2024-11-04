from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data
    user = RegisterSerializer(data=data)
    
    if user.is_valid():
        if User.objects.filter(email=data['email']).exists():
            return Response({"error":"This Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                username = data['username'],
                email = data['email'],
                password = make_password(data['password']),
            )
            return Response({'details':'Your account registered susccessfully!'},status=status.HTTP_201_CREATED)
    else:
        return Response(user.errors)
