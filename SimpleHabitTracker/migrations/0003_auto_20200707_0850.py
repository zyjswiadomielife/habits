# Generated by Django 2.1.5 on 2020-07-07 08:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SimpleHabitTracker', '0002_auto_20200707_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='dayslist',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
