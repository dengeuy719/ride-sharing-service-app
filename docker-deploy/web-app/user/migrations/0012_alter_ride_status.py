# Generated by Django 4.1.6 on 2023-02-07 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_driver_vehicle_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Completed', 'Completed'), ('Confirmed', 'Confirmed')], default='Open', max_length=32),
        ),
    ]
