from django.db import models

from django.contrib.auth.models import AbstractUser

from django.templatetags.static import static

import re

# Create your models here.


class User(AbstractUser):
    is_tl = models.BooleanField(default=False)
    is_judge = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    RANK_CHOICES = (
        ('black', 'Black Belt'),
        ('black_jr', 'Jr. Black Belt'),
        ('red', 'Red Belt'),
        ('brown', 'Brown Belt'),
        ('brown_sr', 'Brown Sr. Belt'),
        ('blue', 'Blue Belt'),
        ('blue_sr', 'Blue Sr. Belt'),
        ('purple', 'Purple Belt'),
        ('green', 'Green Belt'),
        ('orange', 'Orange Belt'),
        ('yellow', 'Yellow Belt'),
        ('white', 'White Belt'),
    )

    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length=7, choices=GENDER_CHOICES, default='male')
    country = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    rank = models.CharField(
        max_length=12, choices=RANK_CHOICES, default='black')

    profile_picture = models.ImageField(
        upload_to='images/profile_pics', null=True, blank=True)

    username = models.CharField(
        max_length=30, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'gender', 'phone', 'country', 'rank', 'username']

    def save(self, *args, **kwargs):
        self.country = re.sub("[\(\[].*?[\)\]]", "", self.country)
        super(User, self).save(*args, **kwargs)

    def get_prof_pic_url(self):
        if not self.profile_picture:
            return static('images/'+('default_boy.png' if self.gender == 'male' else 'default_girl.png'))
        return self.profile_picture.url


class TeamLeaderModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    club_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.email


class JudgeModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.email
