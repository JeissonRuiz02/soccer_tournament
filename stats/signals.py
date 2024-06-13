import json
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MatchResult


@receiver(post_save, sender=MatchResult)
def save_results_to_json(sender, instance, **kwargs):
    """
    Signal receiver that saves match results to a JSON file whenever a MatchResult is saved.
    """
    # Get the tournament associated with the match
    tournament = instance.match.tournament

    # Retrieve all match results for the tournament
    results = MatchResult.objects.filter(match__tournament=tournament)

    # Create a list of result dictionaries
    results_list = []
    for result in results:
        results_list.append({
            'match': str(result.match),  # Match string representation
            'team': result.team.name,  # Team name
            'goals': result.goals,  # Goals scored by the team
            'is_home_team': result.is_home_team,  # Boolean indicating if the team is the home team
            'tournament': result.match.tournament.name,  # Tournament name
            'date': result.match.date.strftime('%Y-%m-%d'),  # Match date in YYYY-MM-DD format
        })

    # Define the file path for the JSON file
    file_path = os.path.join('backups', f'{tournament.name}_results.json')

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write the results to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(results_list, json_file, indent=4)
