# Generated by Django 3.1.12 on 2021-07-07 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0015_auto_20210419_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cert_bg',
            field=models.ImageField(blank=True, null=True, upload_to='images/cert_bg'),
        ),
        migrations.AddField(
            model_name='event',
            name='id_bg',
            field=models.ImageField(blank=True, null=True, upload_to='images/id_bg'),
        ),
    ]
