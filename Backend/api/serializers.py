from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from .models import Profile, Friend
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

#ProfileSerializer
class ProfileSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user','avatar','image_path',]
        extra_kwargs = {
            'image': {
                'write_only' : True,
            }
        }
    def get_image_path(self ,obj):
        return obj.image.url

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
"""
class FriendSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Friend
        fields = ('user', 'friend', 'created_at')
        readonly_fields = 'created_at'

class CustomUsersSerializer(HyperlinkedModelSerializer):
    friends = FriendSerializer(many=True)  

    class Meta:
        models = User
        fields = ('email', 'username', 'password1', 'friends')
"""        