# Generated by Django 3.1.7 on 2021-03-08 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team_leader', '0003_auto_20210308_2216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='dob',
            new_name='date_of_birth',
        ),
    ]
