from django.db import models

# Create your models here.

from team_leader.models import Player, Team


class Event(models.Model):
    title = models.CharField(max_length=100)
    event_banner = models.ImageField(upload_to='images/event_banners')

    event_date = models.DateField()
    reg_deadline = models.DateField()

    contact = models.CharField(max_length=50)
    place = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class RegisteredTeam(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, null=True, blank=True)

    payment_done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.team.name


class RegisteredPlayer(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(
        RegisteredTeam, on_delete=models.CASCADE, null=True, blank=True)

    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, null=True, blank=True)

    certificate = models.ImageField(
        upload_to='images/certificates', null=True, blank=True)

    def __str__(self) -> str:
        return self.player.name
