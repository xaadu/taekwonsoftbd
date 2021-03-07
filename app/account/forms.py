from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, TeamLeaderModel


class TLRegistrationForm(UserCreationForm):

    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'tel', 'id': 'id_telephone'}))

    profile_picture = forms.ImageField(required=False)

    club_name = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',
                  'password1', 'password2',
                  'first_name', 'last_name',
                  'country', 'phone',
                  'gender', 'rank',
                  'club_name', 'profile_picture')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tl = True
        user.is_admin = False
        user.save()

        club_name = self.cleaned_data.get('club_name')
        TeamLeaderModel.objects.create(user=user, club_name=club_name)

        return user
