import os
import json
from django.core.management.base import BaseCommand
from stats.models import Match, Team, Tournament, MatchResult

class Command(BaseCommand):
    help = 'Load match results from JSON backup files'

    def handle(self, *args, **options):
        backup_dir = 'backups'
        for filename in os.listdir(backup_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(backup_dir, filename)
                self.stdout.write(self.style.NOTICE(f'Loading data from {file_path}'))
                with open(file_path, 'r') as json_file:
                    results = json.load(json_file)
                    for result in results:
                        match_str = result['match']
                        try:
                            home_team_name, match_details = match_str.split(' vs ')
                            away_team_name, match_date = match_details.split(' on ')
                            home_team = Team.objects.get(name=home_team_name.strip())
                            away_team = Team.objects.get(name=away_team_name.strip())
                            tournament = Tournament.objects.get(name=result['tournament'])
                            match, created = Match.objects.get_or_create(
                                home_team=home_team,
                                away_team=away_team,
                                date=match_date.strip(),
                                tournament=tournament
                            )
                            MatchResult.objects.create(
                                match=match,
                                team=Team.objects.get(name=result['team']),
                                goals=result['goals'],
                                is_home_team=result['is_home_team']
                            )
                        except ValueError as e:
                            self.stdout.write(self.style.ERROR(f'Error parsing match string: {match_str}'))
                            self.stdout.write(self.style.ERROR(str(e)))
                        except Team.DoesNotExist as e:
                            self.stdout.write(self.style.ERROR(f'Team not found: {str(e)}'))
                        except Tournament.DoesNotExist as e:
                            self.stdout.write(self.style.ERROR(f'Tournament not found: {str(e)}'))
        self.stdout.write(self.style.SUCCESS('Successfully loaded match results from JSON backups'))
