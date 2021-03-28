from django.contrib.auth.models import User 
from rest_framework import generics ,permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from knox.models import AuthToken


from .serializers import (
    GetUserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
)

from .models import Profile 
from rest_framework.permissions import BasePermission
class isTheSameUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id==obj.id


class GetUserAPI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    def get_object(self):
        return self.request.user


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self ,request , *args ,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.get(username=username)
        return Response({'Login': 'Successful!'})

class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ProfileAPI(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


