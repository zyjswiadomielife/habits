# Generated by Django 3.0.7 on 2020-06-24 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal_realisation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalrealisation',
            name='completed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='goalrealisation',
            name='failed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='goalrealisation',
            name='percentage',
            field=models.IntegerField(default=0),
        ),
    ]
