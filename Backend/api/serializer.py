from .models import Challenges
from rest_framework import serializers


class ChallengesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenges
        # fields = ['id', 'user', 'textbox', 'image', 'date_posted', 'status']
        fields =['textbox', 'image', 'status']
