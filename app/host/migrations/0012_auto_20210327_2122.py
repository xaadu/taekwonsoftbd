# Generated by Django 3.1.7 on 2021-03-27 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0011_event_allow_reg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='allow_reg',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True),
        ),
    ]
