from django.db import models

from datetime import date

# Create your models here.

#from team_leader.models import Player, Team


class Event(models.Model):
    title = models.CharField(max_length=100)
    event_banner = models.ImageField(upload_to='images/event_banners')

    event_date = models.DateField()
    reg_deadline = models.DateField()

    judge_1 = models.ForeignKey(
        'account.JudgeModel', on_delete=models.SET_NULL, null=True, related_name='Judge1')
    judge_2 = models.ForeignKey(
        'account.JudgeModel', on_delete=models.SET_NULL, null=True, related_name='Judge2')
    judge_3 = models.ForeignKey(
        'account.JudgeModel', on_delete=models.SET_NULL, null=True, related_name='Judge3')

    contact = models.CharField(max_length=50)
    place = models.CharField(max_length=50)

    outline = models.FileField(upload_to='outlines/', null=True, blank=True)
    REG_CHOICES = ((True, 'Yes'), (False, 'No'))
    allow_reg = models.BooleanField(choices=REG_CHOICES, default=True)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    round = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.name


class RegisteredTeam(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(
        'team_leader.Team', on_delete=models.CASCADE, null=True, blank=True)

    PAYMENT_CHOICES = ((True, 'Yes'), (False, 'No'))
    payment_done = models.BooleanField(choices=PAYMENT_CHOICES, default=True)

    def __str__(self) -> str:
        return self.team.name


class RegisteredPlayer(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(
        RegisteredTeam, on_delete=models.CASCADE, null=True, blank=True)

    player = models.ForeignKey(
        'team_leader.Player', on_delete=models.CASCADE, null=True, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)

    certificate = models.ImageField(
        upload_to='images/certificates', null=True, blank=True)

    def __str__(self) -> str:
        return self.player.name


class PlayerResult(models.Model):
    player = models.ForeignKey(RegisteredPlayer, on_delete=models.CASCADE)
    judge = models.ForeignKey(
        'account.JudgeModel', on_delete=models.SET_NULL, null=True)
    round = models.IntegerField()
    accuracy = models.FloatField(default=0)
    presentation = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.player.player.name + '(Round: ' + str(self.round) + ')'
