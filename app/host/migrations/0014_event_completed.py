# Generated by Django 3.1.7 on 2021-03-28 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0013_auto_20210327_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='completed',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]
