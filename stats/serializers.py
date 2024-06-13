from rest_framework import serializers
from .models import Team, Tournament, Match, TeamTournamentStats


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class TeamTournamentStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTournamentStats
        fields = '__all__'
