from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import Player, Team
from account.models import User


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


class TLUpdateForm(UserChangeForm):
    club_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'tel', 'id': 'id_telephone'}))
    password = None  # Else shows password field

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'country', 'phone',
            'rank', 'gender',
            'club_name',
            'profile_picture',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['club_name'].initial = self.request.user.teamleadermodel.club_name
