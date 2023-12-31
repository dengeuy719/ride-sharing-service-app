# Generated by Django 4.1.5 on 2023-02-03 03:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(blank=True, max_length=256, null=True)),
                ('plate_num', models.CharField(blank=True, max_length=256, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('special_vehicle_info', models.TextField(blank=True, max_length=256, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='driver2_user_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('destination', models.CharField(max_length=256)),
                ('arrival_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('passenger_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('is_shared', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Confirmed', 'Confirmed'), ('Completed', 'Completed'), ('Open', 'Open')], default='Open', max_length=32)),
                ('special_request', models.CharField(blank=True, default='', max_length=256)),
                ('special_vehicle_type', models.CharField(blank=True, default='', max_length=256)),
                ('completed', models.BooleanField(default=False)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_user_set', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_user_set', to=settings.AUTH_USER_MODEL)),
                ('sharer', models.ManyToManyField(blank=True, related_name='sharer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('is_driver', 'is_driver'),),
            },
        ),
        migrations.DeleteModel(
            name='Driver1',
        ),
    ]
