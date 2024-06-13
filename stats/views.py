from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Match, Tournament, TeamTournamentStats, MatchResult
from .forms import MatchForm, TeamForm, TournamentForm


# View to enter a match result and update statistics
def enter_result(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == 'POST':
        form = MatchForm(request.POST, tournament=tournament)
        if form.is_valid():
            match = form.save(commit=False)
            match.tournament = tournament
            match.save()

            # Register the match results for both teams
            MatchResult.objects.create(match=match, team=match.home_team, goals=match.home_goals, is_home_team=True)
            MatchResult.objects.create(match=match, team=match.away_team, goals=match.away_goals, is_home_team=False)

            # Update team statistics
            update_statistics(match)
            return redirect('stats:league_table', tournament_id=tournament.id)
    else:
        form = MatchForm(tournament=tournament)

    return render(request, 'stats/enter_result.html', {'form': form, 'tournament': tournament})


# Helper function to update team statistics after a match
def update_statistics(match):
    home_team_stats, created = TeamTournamentStats.objects.get_or_create(team=match.home_team, tournament=match.tournament)
    away_team_stats, created = TeamTournamentStats.objects.get_or_create(team=match.away_team, tournament=match.tournament)

    home_team_stats.matches_played += 1
    away_team_stats.matches_played += 1

    home_team_stats.goals_for += match.home_goals
    home_team_stats.goals_against += match.away_goals
    away_team_stats.goals_for += match.away_goals
    away_team_stats.goals_against += match.home_goals

    if match.home_goals > match.away_goals:
        home_team_stats.matches_won += 1
        home_team_stats.points += 3
        away_team_stats.matches_lost += 1
    elif match.home_goals < match.away_goals:
        away_team_stats.matches_won += 1
        away_team_stats.points += 3
        home_team_stats.matches_lost += 1
    else:
        home_team_stats.matches_drawn += 1
        away_team_stats.matches_drawn += 1
        home_team_stats.points += 1
        away_team_stats.points += 1

    home_team_stats.save()
    away_team_stats.save()


# View to delete a tournament
def delete_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == 'POST':
        tournament.delete()
        return redirect('stats:tournament_list')

    return render(request, 'stats/delete_tournament.html', {'tournament': tournament})


# View to display the league table for a tournament
def league_table(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    stats = TeamTournamentStats.objects.filter(tournament=tournament).order_by('-points', '-goals_for', '-goals_against')
    for stat in stats:
        stat.goal_difference = stat.goals_for - stat.goals_against  # Calculate goal difference
    return render(request, 'stats/league_table.html', {'tournament': tournament, 'stats': stats})


# View to list all teams
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'stats/team_list.html', {'teams': teams})


# View to add a new team
def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stats:team_list')
    else:
        form = TeamForm()
    return render(request, 'stats/add_team.html', {'form': form})


# View to edit an existing team
def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('stats:team_list')
    else:
        form = TeamForm(instance=team)
    return render(request, 'stats/edit_team.html', {'form': form})


# View to delete a team
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        team.delete()
        return redirect('stats:team_list')
    return render(request, 'stats/delete_team.html', {'team': team})


# View to list all tournaments
def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'stats/tournament_list.html', {'tournaments': tournaments})


# View to add a new tournament
def add_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            teams = form.cleaned_data['teams']
            for team in teams:
                TeamTournamentStats.objects.create(team=team, tournament=tournament)
            return redirect('stats:tournament_list')
    else:
        form = TournamentForm()
    return render(request, 'stats/add_tournament.html', {'form': form})


# View to display details of a tournament and its teams
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    teams = Team.objects.filter(teamtournamentstats__tournament=tournament)
    return render(request, 'stats/tournament_detail.html', {'tournament': tournament, 'teams': teams})


# View to display match results for a specific team
def match_results(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    results = MatchResult.objects.filter(team=team).order_by('-match__date')
    return render(request, 'stats/match_results.html', {'team': team, 'results': results})


# View to export match results to JSON for a tournament
def export_json(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    results = MatchResult.objects.filter(match__tournament=tournament)

    results_list = []
    for result in results:
        results_list.append({
            'match': str(result.match),
            'team': result.team.name,
            'goals': result.goals,
            'is_home_team': result.is_home_team,
            'tournament': result.match.tournament.name,
            'date': result.match.date,
        })

    return JsonResponse(results_list, safe=False)
