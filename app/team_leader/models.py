from account.models import TeamLeaderModel
from django.db import models

import re

# Create your models here.


class Player(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    teamleader = models.ForeignKey(TeamLeaderModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=7, choices=GENDER_CHOICES, default='male')
    date_of_birth = models.DateField()
    country = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    picture = models.ImageField(
        upload_to='images/player')

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
