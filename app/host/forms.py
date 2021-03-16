from django import forms
from django.contrib.auth.forms import UserChangeForm

from account.models import User

from .models import Event, Category


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


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
