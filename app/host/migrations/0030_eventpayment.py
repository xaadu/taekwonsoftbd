# Generated by Django 3.1.14 on 2023-06-10 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20230501_1716'),
        ('host', '0029_auto_20230604_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_total', models.FloatField(default=0.0)),
                ('amount_paid', models.FloatField(default=0.0)),
                ('is_paid', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='host.event')),
                ('teamleader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.teamleadermodel')),
            ],
        ),
    ]
