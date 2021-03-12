from django.urls import path
from .views import *

app_name = 'home'
urlpatterns = [
    path('', comingsoon, name='comingsoon'),
    path('events/', events, name='events'),
    path('events/<str:pk>/', event_details, name='event_details'),
    path('events/<str:pk>/apply/', apply, name='apply'),
]
