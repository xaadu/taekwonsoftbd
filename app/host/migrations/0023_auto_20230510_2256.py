# Generated by Django 3.1.14 on 2023-05-10 22:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0022_registeredmember'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='num_of_player',
        ),
        migrations.AddField(
            model_name='category',
            name='extra_players',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
