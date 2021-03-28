from .models import Challenges
from rest_framework import serializers


class ChallengesSerializer(serializers.ModelSerializer):
    # need to return primary key in response


    class Meta:
        model = Challenges
        # fields = ['id', 'user', 'textbox', 'image', 'date_posted', 'status']

        fields = ['id', 'proposer', 'user', 'title', 'description', 'image', 'date_posted', 'status']
