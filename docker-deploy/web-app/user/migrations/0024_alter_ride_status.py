# Generated by Django 4.1.6 on 2023-02-07 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_alter_ride_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='status',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Open', 'Open'), ('Completed', 'Completed')], default='Open', max_length=32),
        ),
    ]
