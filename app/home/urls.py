from django.urls import path
from .views import *

app_name = 'home'
urlpatterns = [
    #path('', comingsoon, name='comingsoon'),
    path('', home, name='home'),
    path('events/', events, name='events'),
    path('events/<str:pk>/', event_details, name='event_details'),
    path('events/<str:pk>/teams/', event_teams, name='teams'),
    path('events/<str:event_id>/teams/<str:reg_team_id>/',
         event_team_details, name='team_details'),
    path('events/<str:pk>/players/', event_players, name='players'),
    path('events/<str:pk>/manage/', manage, name='manage'),
    path('events/<str:event_id>/manage/<str:reg_team_id>/',
         event_team_update, name='update_team'),
    path('events/<str:event_id>/delete/<str:reg_team_id>/',
         event_team_delete, name='delete_team'),
    path('events/<str:pk>/apply/', apply, name='apply'),
    path('events/<int:event_id>/results/',
         result_categories, name='result_categories'),
    path('events/<int:event_id>/results/<int:category_id>/',
         results, name='results'),
]
