# Generated by Django 2.1.5 on 2020-07-07 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SimpleHabitTracker', '0003_auto_20200707_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='dayslist',
        ),
    ]
