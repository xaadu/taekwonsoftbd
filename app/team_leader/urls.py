from django.urls import path
from .views import (
    dashboard,
    player_list,
    team_list,
    add_player,
    add_team,
    update_player,
    update_team,
)

app_name = 'team_leader'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('players/', player_list, name='players'),
    path('teams/', team_list, name='teams'),
    path('add_player/', add_player, name='add_player'),
    path('add_team/', add_team, name='add_team'),
    path('update_player/', update_player, name='update_player'),
    path('update_team/', update_team, name='update_team'),
]
