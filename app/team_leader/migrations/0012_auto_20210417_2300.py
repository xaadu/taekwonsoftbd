# Generated by Django 3.1.7 on 2021-04-17 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_leader', '0011_auto_20210417_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='member_Type',
            field=models.CharField(choices=[('player', 'Player'), ('coach', 'Coach'), ('doctor', 'Doctor'), ('manager', 'Manager'), ('guardian', 'Guardian'), ('owner', 'Owner'), ('instructor', 'Instructor'), ('team_official', 'Team Official'), ('media', 'Media'), ('volunteer', 'Vaulenteer'), ('referee', 'Referee')], default='player', max_length=20),
        ),
    ]