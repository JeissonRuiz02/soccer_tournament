from django.urls import path
from . import views

app_name = 'stats'
urlpatterns = [
    path('enter_result/<int:tournament_id>/', views.enter_result, name='enter_result'),
    path('league_table/<int:tournament_id>/', views.league_table, name='league_table'),
    path('teams/', views.team_list, name='team_list'),
    path('teams/add/', views.add_team, name='add_team'),
    path('teams/edit/<int:team_id>/', views.edit_team, name='edit_team'),
    path('teams/delete/<int:team_id>/', views.delete_team, name='delete_team'),
    path('tournaments/', views.tournament_list, name='tournament_list'),
    path('tournaments/add/', views.add_tournament, name='add_tournament'),
    path('tournaments/<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    path('tournaments/delete/<int:tournament_id>/', views.delete_tournament, name='delete_tournament'),
    path('match_results/<int:team_id>/', views.match_results, name='match_results'),
    path('export_json/<int:tournament_id>/', views.export_json, name='export_json'),  # Nueva URL para exportar datos en JSON
]
