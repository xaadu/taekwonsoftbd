from django.urls import path
from .views import *

app_name = 'stream'
urlpatterns = [
    path('events/', events, name='events'),
    path('events/<int:event_id>/players/', players, name='players'),
    path('events/<int:event_id>/players/<int:reg_player_id>/<int:round>/',
         playerDetails, name='playerDetails'),
]
