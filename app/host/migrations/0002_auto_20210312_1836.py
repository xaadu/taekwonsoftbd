# Generated by Django 3.1.7 on 2021-03-12 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team_leader', '0008_auto_20210309_0043'),
        ('host', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registeredplayer',
            name='player',
        ),
        migrations.AddField(
            model_name='registeredplayer',
            name='player',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='team_leader.player'),
        ),
        migrations.RemoveField(
            model_name='registeredteam',
            name='team',
        ),
        migrations.AddField(
            model_name='registeredteam',
            name='team',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='team_leader.team'),
        ),
    ]
