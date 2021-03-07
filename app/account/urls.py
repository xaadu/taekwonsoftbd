from os import name
from django.urls import path
from .views import (
    registration_view,
    judge_registration_view,
    logout_view,
    login_view,
    sample
)

app_name = 'account'
urlpatterns = [
    path('sample/', sample, name='sample'),
    path('register/', registration_view, name='register'),
    path('judge_register/', judge_registration_view, name='judge_register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login')
]
