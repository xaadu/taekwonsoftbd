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
        ('10th_gup', '10th Gup'),
        ('9th_gup', '9th Gup'),
        ('8th_gup', '8th Gup'),
        ('7th_gup', '7th Gup'),
        ('6th_gup', '6th Gup'),
        ('5th_gup', '5th Gup'),
        ('4th_gup', '4th Gup'),
        ('3rd_gup', '3rd Gup'),
        ('2nd_gup', '2nd Gup'),
        ('1st_gup', '1st Gup'),
        ('4th_poom', '4th Poom'),
        ('3rd_poom', '3rd Poom'),
        ('2nd_poom', '2nd Poom'),
        ('1st_poom', '1st Poom'),
        ('9th_dan', '9th Dan'),
        ('8th_dan', '8th Dan'),
        ('7th_dan', '7th Dan'),
        ('6th_dan', '6th Dan'),
        ('5th_dan', '5th Dan'),
        ('4th_dan', '4th Dan'),
        ('3rd_dan', '3rd Dan'),
        ('2nd_dan', '2nd Dan'),
        ('1st_dan', '1st Dan'),
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
