from typing import Iterable, Optional
from django.core.validators import MaxValueValidator, MinValueValidator 
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
    venue = models.CharField(max_length=50)

    outline = models.FileField(upload_to='outlines/', null=True, blank=True)

    id_bg = models.ImageField(upload_to='images/id_bg', blank=True, null=True)
    cert_bg = models.ImageField(upload_to='images/cert_bg', blank=True, null=True)

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    allow_reg = models.BooleanField(choices=BOOL_CHOICES, default=False)
    allow_manage = models.BooleanField(choices=BOOL_CHOICES, default=True)
    allow_payment = models.BooleanField(choices=BOOL_CHOICES, default=False)
    completed = models.BooleanField(choices=BOOL_CHOICES, default=False)

    def __str__(self) -> str:
        return self.title



class Category(models.Model):
 
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    extra_players = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    # TODO: round should be in subcategory
    round = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):

    MALE = 'male'
    FEMALE = 'female'

    CHOICES__GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=100)
    
    min_age = models.PositiveSmallIntegerField(validators=[MinValueValidator(2), MaxValueValidator(100)])
    max_age = models.PositiveSmallIntegerField(validators=[MinValueValidator(2), MaxValueValidator(100)])
    gender = models.CharField(max_length=6, choices=CHOICES__GENDER)

    def __str__(self) -> str:
        return self.title



class RegisteredMember(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    member = models.ForeignKey('team_leader.Player', on_delete=models.CASCADE, null=True)
    team = models.ForeignKey('team_leader.Team', on_delete=models.CASCADE, null=True)

    has_parent = models.BooleanField(default=False)
    parent_member = models.ForeignKey(
        to='self',
        limit_choices_to={'has_parent': False},
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='submembers'
    )

    PAYMENT_CHOICES = ((True, 'Yes'), (False, 'No'))
    payment_done = models.BooleanField(choices=PAYMENT_CHOICES, default=False)

    def __str__(self) -> str:
        return self.member.name



class EventPayment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    teamleader = models.ForeignKey("account.TeamLeaderModel", on_delete=models.CASCADE)
    
    amount_total = models.FloatField(default=0.0)
    amount_paid = models.FloatField(default=0.0)
    
    PAYMENT_CHOICES = ((True, 'Yes'), (False, 'No'))
    is_paid = models.BooleanField(choices=PAYMENT_CHOICES, default=False)





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
