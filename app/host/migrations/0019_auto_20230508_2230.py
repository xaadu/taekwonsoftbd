# Generated by Django 3.1.14 on 2023-05-08 22:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0018_auto_20230508_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='num_of_player',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
