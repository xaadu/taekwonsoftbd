from django.urls import path
from .views import (
    dashboard,
    profile,
    create_event,
    events,
    event_details,
)

app_name = 'host'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('events/', events, name='events'),
    path('events/create/', create_event, name='create_event'),
    path('events/<str:pk>/', event_details, name='event_details'),
]
