from rest_framework import serializers

from teams.models import Team, Player

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ["id", "first_name", "last_name"]

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team