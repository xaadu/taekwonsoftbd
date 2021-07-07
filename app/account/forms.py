from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import JudgeModel, User, TeamLeaderModel


class TLRegistrationForm(UserCreationForm):

    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'tel', 'id': 'id_telephone'}))
    profile_picture = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=60, required=True)
    last_name = forms.CharField(max_length=60, required=True)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].label = 'Email Address'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['phone'].label = 'Phone Number'
        self.fields['club_name'].label = 'Club Name'
        self.fields['profile_picture'].label = 'Profile Picture'

        # self.fields[''].label = ''

        for key, value in self.fields.items():
            label = value.label
            if value.required and label:
                label = label+'*'
                self.fields[key].label = label


class JudgeRegistrationForm(UserCreationForm):

    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'tel', 'id': 'id_telephone'}))
    profile_picture = forms.ImageField(required=True)
    first_name = forms.CharField(max_length=60, required=True)
    last_name = forms.CharField(max_length=60, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',
                  'password1', 'password2',
                  'first_name', 'last_name',
                  'country', 'phone',
                  'gender', 'rank',
                  'profile_picture')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_judge = True
        user.is_admin = False
        user.save()

        JudgeModel.objects.create(user=user)

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].label = 'Email Address'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['phone'].label = 'Phone Number'
        self.fields['profile_picture'].label = 'Profile Picture'

        # self.fields[''].label = ''

        for key, value in self.fields.items():
            label = value.label
            if value.required and label:
                label = label+'*'
                self.fields[key].label = label
