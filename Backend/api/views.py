from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from django.db.models import Q
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
        return request.user.id == obj.id


class GetUserAPI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer

    def get_object(self):
        return self.request.user


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
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


# ------------------------------------------------#
# TRIAL
from .serializers import FriendSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from .models import Friend
from rest_framework import status, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    # profile searching
    search_fields = ['user__username', ]
    filter_backends = [filters.SearchFilter]
    permission_classes =[AllowAny,]

    # exclude from search result user himself & user friends
    def get_queryset(self):
        user_friends_ids = Friend.objects.filter(user=self.request.user.id).values_list('friend_id', flat=True)
        qs = self.queryset
        return qs

    def retrieve(self, request, *args, **kwargs):
        """
        LIST OF PROFILES
        """
        try:
            user_id = kwargs.get('pk')
            qs = self.queryset.get(user_id=user_id)
            serializer = self.serializer_class(qs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FriendViewSet(ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = [AllowAny, ]

    def retrieve(self, request, *args, **kwargs):
        """
        USER'S FRIEND LIST
        """
        try:
            user_id = kwargs.get('pk')
            user_friends = self.queryset.filter(user_id=user_id)
            friends_profiles = [Profile.objects.get(user_id=friend.friend.id) for friend in user_friends]
            data = ProfileSerializer(friends_profiles, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        UNFRIEND USER
        """
        try:
            user_id = kwargs.get('pk')
            friend_id = request.data.get('friend_id')
            user_friend = self.queryset.filter(Q(user_id=user_id) & Q(friend_id=friend_id))
            user_friend.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


from .models import Challenges
from .serializers import ChallengesSerializer
from rest_framework.decorators import api_view


def get_challenge(pk):
    return Challenges.objects.get(pk=pk)


@api_view(['GET', 'POST', 'PUT'])
def challenges_list(request):
    if request.method == 'GET':
        # straight away sort by status first
        challenges = Challenges.objects.order_by('status').all()
        username = request.POST.get("user", None)
        # img_path = request.POST.get("image_path", False)
        # Filter by username
        if username:
            challenges = challenges.filter(user=username)

        serializer = ChallengesSerializer(challenges, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ChallengesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        id = request.POST.get("id", None)
        if id is None:
            return
        serializer = ChallengesSerializer(get_challenge(id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
