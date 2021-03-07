from django.urls import path
from .views import comingsoon

app_name = 'home'
urlpatterns = [
    path('', comingsoon, name='comingsoon'),
]
