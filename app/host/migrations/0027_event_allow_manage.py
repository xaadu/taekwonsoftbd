# Generated by Django 3.1.14 on 2023-06-04 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0026_auto_20230514_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allow_manage',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]