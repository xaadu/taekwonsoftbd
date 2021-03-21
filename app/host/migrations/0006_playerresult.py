# Generated by Django 3.1.7 on 2021-03-21 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('host', '0005_category_round'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField(unique=True)),
                ('judge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.judgemodel')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='host.registeredplayer')),
            ],
        ),
    ]
