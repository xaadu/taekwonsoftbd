from django import forms
from django.db import transaction

from .models import Player


class PlayerCreateForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        exclude = ['teamleader']
