from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    tournaments = models.ManyToManyField('Tournament', through='TeamTournamentStats', related_name='teams')

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    home_goals = models.IntegerField()
    away_goals = models.IntegerField()
    date = models.DateField()
    tournament = models.ForeignKey(Tournament, related_name='matches', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.home_team} vs {self.away_team} on {self.date}'


class TeamTournamentStats(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    matches_lost = models.IntegerField(default=0)
    matches_drawn = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ('team', 'tournament')

    def __str__(self):
        return f'{self.team} in {self.tournament}'


class MatchResult(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    goals = models.IntegerField()
    is_home_team = models.BooleanField()

    def __str__(self):
        return f'{self.team} in {self.match}'
