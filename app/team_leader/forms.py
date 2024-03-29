from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import Player, Team
from account.models import User


class PlayerCreateForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = '__all__'
        exclude = ['teamleader']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Full Name'
        self.fields['passport_or_ID_Card'].label = 'Passport/NID/Birth Certificate'
        self.fields['date_Of_Birth'].widget = forms.DateInput(
            format=('%m/%d/%Y'), attrs={'type': 'date'})

        for key, value in self.fields.items():
            label = value.label
            if value.required:
                label = label+'*'
                self.fields[key].label = label


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        exclude = ['teamleader']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = 'Team Name'

        for key, value in self.fields.items():
            label = value.label
            if value.required:
                label = label+'*'
                self.fields[key].label = label


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
