# Generated by Django 3.1.7 on 2021-04-19 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0014_event_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='place',
            new_name='venue',
        ),
    ]
