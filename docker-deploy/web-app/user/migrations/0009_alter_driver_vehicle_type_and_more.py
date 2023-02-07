# Generated by Django 4.1.5 on 2023-02-05 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_driver_vehicle_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='vehicle_type',
            field=models.CharField(choices=[('6', 'Pickup'), ('4', 'Sedan'), ('4', 'Coupe'), ('5', 'SUV')], max_length=256, verbose_name='Vehicle Type'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='special_vehicle_type',
            field=models.IntegerField(blank=True, choices=[(4, 'Sedan'), (3, 'Coupe'), (5, 'SUV'), (6, 'Pcikup')], null=True, verbose_name='special_vehicle_type'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Completed', 'Completed'), ('Confirmed', 'Confirmed')], default='Open', max_length=32),
        ),
    ]
