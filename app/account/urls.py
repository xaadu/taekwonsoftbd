from os import name
from django.urls import path
from .views import (
    registration_view,
    sample
)

app_name = 'account'
urlpatterns = [
    path('sample/', sample, name='sample'),
    path('register/', registration_view, name='register'),
]
