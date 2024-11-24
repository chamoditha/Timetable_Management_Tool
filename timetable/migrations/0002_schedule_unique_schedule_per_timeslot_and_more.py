# Generated by Django 5.1.3 on 2024-11-21 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='schedule',
            constraint=models.UniqueConstraint(fields=('day', 'timeslot', 'year'), name='unique_schedule_per_timeslot'),
        ),
        migrations.AddConstraint(
            model_name='schedule',
            constraint=models.UniqueConstraint(fields=('day', 'timeslot', 'lecturer'), name='unique_lecturer_per_timeslot'),
        ),
        migrations.AddConstraint(
            model_name='schedule',
            constraint=models.UniqueConstraint(fields=('day', 'timeslot', 'hall'), name='unique_hall_per_timeslot'),
        ),
    ]
