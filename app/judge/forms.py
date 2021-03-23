from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.db.models import fields

from account.models import User
from host.models import PlayerResult


class JudgeUpdateForm(UserChangeForm):
    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'tel', 'id': 'id_telephone'}))
    profile_picture = forms.ImageField(required=True)
    password = None  # Else shows password field

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'country', 'phone',
            'rank', 'gender',
            'profile_picture',
        ]


class MarkingForm(forms.ModelForm):
    presentation = forms.FloatField(max_value=4.0, min_value=0.0)
    accuracy = forms.FloatField(max_value=6.0, min_value=0.0)

    class Meta:
        model = PlayerResult
        fields = ['presentation', 'accuracy']
