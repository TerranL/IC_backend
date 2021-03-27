from Backend.api.models import Challenges
from rest_framework import serializers


class ChallengesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenges
        fields = ['user', 'textbox', 'image', 'date_posted', 'status']
