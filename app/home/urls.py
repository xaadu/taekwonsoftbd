from django.urls import path
from .views import comingsoon

urlpatterns = [
    path('', comingsoon, name='comingsoon'),
]
