# Generated by Django 3.1.12 on 2021-07-07 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team_leader', '0014_auto_20210418_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='member_Type',
        ),
    ]
