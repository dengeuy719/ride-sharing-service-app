# Generated by Django 4.1.6 on 2023-02-07 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_alter_ride_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Open', 'Open'), ('Confirmed', 'Confirmed')], default='Open', max_length=32),
        ),
    ]