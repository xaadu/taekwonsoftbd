from django import forms
from django.core.exceptions import ValidationError

from host.models import RegisteredMember, RegisteredTeam


class PlayerApplyForm(forms.ModelForm):
    class Meta:
        model = RegisteredTeam
        fields = ['team']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        teams = self.request.user.teamleadermodel.team_set.all()
        players = self.request.user.teamleadermodel.player_set.all()
        self.fields['team'] = forms.ModelChoiceField(
            required=True, queryset=teams, widget=forms.Select())
        self.fields['players'] = forms.ModelMultipleChoiceField(
            required=True, queryset=players, widget=forms.CheckboxSelectMultiple())


class PlayerUpdateForm(forms.ModelForm):
    secret = forms.CharField(max_length=1000, widget=forms.HiddenInput())

    class Meta:
        model = RegisteredTeam
        fields = ['secret']

    def __init__(self, *args, **kwargs):
        self.players = kwargs.pop("players")
        super().__init__(*args, **kwargs)
        self.fields['players'] = forms.ModelMultipleChoiceField(
            required=True, queryset=self.players, widget=forms.CheckboxSelectMultiple())



class MemberApplyForm(forms.ModelForm):
    class Meta:
        model = RegisteredMember
        fields = ['sub_category']

    def __init__(self, *args, **kwargs):
        self.subcategories = kwargs.pop("subcategories")
        
        super().__init__(*args, **kwargs)

        self.fields['sub_category'].queryset = self.subcategories


class SubMemberApplyForm(forms.ModelForm):

    class Meta:
        model=RegisteredMember
        fields = ['member']

    def __init__(self, *args, **kwargs):
        self.submembers = kwargs.pop("submembers")
        
        super().__init__(*args, **kwargs)

        self.fields['member'].qs = self.submembers


class SubMemberApplyForm2(forms.Form):
    members = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    class Meta:
        fields = ['members']

    def __init__(self, *args, **kwargs):
        self.submembers = kwargs.pop("submembers")
        self.num_of_player = kwargs.pop("num_of_player")
        
        super().__init__(*args, **kwargs)

        self.fields['members'].queryset = self.submembers


    
    def clean(self):

        cleaned_data = super().clean()
        members = cleaned_data.get('members')

        if not members or len(members) != self.num_of_player:
            raise ValidationError(
                f"You must select {self.num_of_player} members."
            )
        




class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
