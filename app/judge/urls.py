from django.urls import path
from .views import (
    dashboard,
    profile,
    players,
    set_point,
)


app_name = 'judge'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('events/<str:event_id>/players', players, name='players'),
    path('events/<str:event_id>/players/<str:player_id>/<int:round>',
         set_point, name='set_point'),
]
