# Generated by Django 3.1.14 on 2023-05-08 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0019_auto_20230508_2230'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('min_age', models.PositiveSmallIntegerField()),
                ('max_age', models.PositiveSmallIntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='host.category')),
            ],
        ),
    ]
