# Generated by Django 3.1.7 on 2021-03-12 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team_leader', '0008_auto_20210309_0043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('event_banner', models.ImageField(upload_to='images/event_banners')),
                ('event_date', models.DateField()),
                ('reg_deadline', models.DateField()),
                ('contact', models.CharField(max_length=50)),
                ('place', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_done', models.BooleanField(default=False)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='host.event')),
                ('team', models.ManyToManyField(blank=True, null=True, to='team_leader.Team')),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.ImageField(upload_to='images/certificates')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='host.event')),
                ('player', models.ManyToManyField(blank=True, null=True, to='team_leader.Player')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='host.registeredteam')),
            ],
        ),
    ]
