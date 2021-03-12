from django import forms

from host.models import RegisteredTeam


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
