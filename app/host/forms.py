from django import forms
from django.contrib.auth.forms import UserChangeForm

from account.models import User


class HostUpdateForm(UserChangeForm):
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
