# Generated by Django 3.1.14 on 2023-07-28 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0030_eventpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('any', 'Any')], max_length=6),
        ),
    ]
