from django import forms
from django.db import transaction

from .models import Player, Team


class PlayerCreateForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        exclude = ['teamleader']


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        exclude = ['teamleader']
