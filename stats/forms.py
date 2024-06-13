from django import forms
from .models import Match, Tournament, Team
from django.core.exceptions import ValidationError


# Custom validator to ensure goal values are non-negative
def validate_non_negative(value):
    if value < 0:
        raise ValidationError('Goals cannot be negative')


# Form for creating or updating Match instances
class MatchForm(forms.ModelForm):
    home_goals = forms.IntegerField(validators=[validate_non_negative])  # Adding non-negative validator for home goals
    away_goals = forms.IntegerField(validators=[validate_non_negative])  # Adding non-negative validator for away goals

    class Meta:
        model = Match
        fields = ['home_team', 'away_team', 'home_goals', 'away_goals', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        tournament = kwargs.pop('tournament', None)
        super(MatchForm, self).__init__(*args, **kwargs)
        if tournament:
            # Limit the queryset of teams to those participating in the given tournament
            self.fields['home_team'].queryset = Team.objects.filter(teamtournamentstats__tournament=tournament)
            self.fields['away_team'].queryset = Team.objects.filter(teamtournamentstats__tournament=tournament)


# Form for creating or updating Team instances
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


# Form for creating or updating Tournament instances
class TournamentForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Tournament
        fields = ['name', 'teams']

    def clean_teams(self):
        teams = self.cleaned_data.get('teams')
        if len(teams) != 20:
            raise forms.ValidationError('You must select exactly 20 teams.')  # Ensure exactly 20 teams are selected
        return teams
