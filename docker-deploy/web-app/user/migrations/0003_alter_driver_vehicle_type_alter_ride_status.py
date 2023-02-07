# Generated by Django 4.1.5 on 2023-02-05 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_driver_ride_delete_driver1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='vehicle_type',
            field=models.CharField(choices=[('Coupe', '4'), ('SUV', '5'), ('Pickup', '6'), ('Sedan', '4')], default='Sedan', max_length=256, verbose_name='Vehicle Type'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='status',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Open', 'Open'), ('Completed', 'Completed')], default='Open', max_length=32),
        ),
    ]