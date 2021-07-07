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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].label = 'Event Title'
        self.fields['event_banner'].label = 'Event Banner Image'
        self.fields['event_date'].label = 'Event Date'
        self.fields['reg_deadline'].label = 'Registration Deadline'

        self.fields['judge_1'].label = 'Main Judge'
        self.fields['judge_2'].label = 'First Judge'
        self.fields['judge_3'].label = 'Second Judge'

        self.fields['id_bg'].label = 'ID Card background'
        self.fields['cert_bg'].label = 'Certificate Background'

        self.fields['allow_reg'].label = 'Allow Registration'
        self.fields['completed'].label = 'Event Completed'

        # self.fields[''].label = ''

        for key, value in self.fields.items():
            label = value.label
            if value.required:
                label = label+'*'
                self.fields[key].label = label


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'round']
