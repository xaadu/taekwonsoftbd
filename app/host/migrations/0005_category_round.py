# Generated by Django 3.1.7 on 2021-03-21 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0004_auto_20210313_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='round',
            field=models.IntegerField(default=1),
        ),
    ]