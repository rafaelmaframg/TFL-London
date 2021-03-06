# Generated by Django 3.2.9 on 2021-11-04 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_name', models.CharField(max_length=5)),
                ('destination_name', models.CharField(max_length=15)),
                ('vehicle_id', models.CharField(max_length=10, unique=True)),
                ('expected_arrival', models.DateTimeField(verbose_name='expected')),
                ('time_now', models.DateTimeField(verbose_name='time Now')),
            ],
        ),
    ]
