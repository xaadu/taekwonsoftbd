from account.models import TeamLeaderModel
from django.db import models
from django.core.exceptions import ValidationError

import re

# Create your models here.


def validate_player_image(image):

    min_height = 300
    min_width = min_height

    height, width = image.height, image.width

    if width < min_width or height < min_height:
        raise ValidationError(f"Upload a Better Quality Image. Minimum resoulation is {min_width} x {min_height}")


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
        ('volunteer', 'Volunteer'),
        ('referee', 'Referee'),
    )

    teamleader = models.ForeignKey(TeamLeaderModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=7, choices=GENDER_CHOICES, default='male')
    date_Of_Birth = models.DateField()
    country = models.CharField(max_length=50)
    #club = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='images/player', validators=[validate_player_image])
    member_Type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default='player')
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
    club_Name = models.CharField(max_length=50, null=True, blank=True)
    team_logo = models.ImageField(upload_to='images/team_logo')
    country = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.country = re.sub("[\(\[].*?[\)\]]", "", self.country)
        super(Team, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
