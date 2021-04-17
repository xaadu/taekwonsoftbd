from account.models import TeamLeaderModel
from django.db import models

import re

# Create your models here.


class Player(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    TYPE_CHOICES = (
        ('player', 'Player'),
        ('coach', 'Coach'),
        ('doctor', 'Doctor'),
        ('manager', 'Manager'),
        ('guardian', 'Guardian'),
        ('owner', 'Owner'),
        ('instructor', 'Instructor'),
        ('team_official', 'Team Official'),
        ('media', 'Media'),
        ('volunteer', 'Vaulenteer'),
        ('referee', 'Referee'),
    )

    teamleader = models.ForeignKey(TeamLeaderModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=7, choices=GENDER_CHOICES, default='male')
    date_Of_Birth = models.DateField()
    country = models.CharField(max_length=50)
    #club = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='images/player')
    member_Type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default='male')
    gMS_Licence_No = models.CharField(max_length=30, null=True, blank=True)
    passport_or_ID_Card = models.ImageField(upload_to='images/passport_or_nid', null=True, blank=True)
    dan_Certificate_No = models.CharField(max_length=30, null=True, blank=True)
    dan_Certificate = models.ImageField(upload_to='images/dan_certificates', null=True, blank=True)


    def save(self, *args, **kwargs):
        self.country = re.sub("[\(\[].*?[\)\]]", "", self.country)
        super(Player, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    teamleader = models.ForeignKey(TeamLeaderModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    district = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.country = re.sub("[\(\[].*?[\)\]]", "", self.country)
        super(Team, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
