from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from .models import Profile, Friend
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)


#ProfileSerializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(partial=True)
    avatar = serializers.URLField() 
    
    class Meta:
        model = Profile
        fields = ['user','avatar','date_of_birth',]


#userInfoSerializer
class GetUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = User 
        fields = ['id','username' ,'email' ,'first_name' ,'last_name','profile']

    def get_profile(self ,obj):
        try :
            profile = obj.profile
            return ProfileSerializer(profile).data
        except :
            return None


#login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self ,data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("username or password Incorrect")

        return data 

#Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,)
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())],)
    password1 = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password],
    )
    password2 = serializers.CharField(
        write_only= True,
        required = True,
    )  

    class Meta:
        model = User 
        fields = (
            'email',
            'username',
            'password1',
            'password2',
            
        )
       
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'error': ['Passwords do not match!']})
        return attrs


    def create(self ,data):
        user = User.objects.create_user(
            email = data['email'],
            username = data['username'],
            password = data['password1'],
        )
        user.save()
        return user

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('user', 'friend')