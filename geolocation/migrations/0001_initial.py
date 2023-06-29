# Generated by Django 3.2.15 on 2023-06-23 12:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, unique=True, verbose_name='Адрес')),
                ('coordinate_lat', models.FloatField(blank=True, default=None, null=True, verbose_name='Широта')),
                ('coordinate_lng', models.FloatField(blank=True, default=None, null=True, verbose_name='Долгота')),
                ('request_datetime', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Время последнего обновления')),
                ('can_determine_coordinates', models.BooleanField(default=True, verbose_name='Определяются ли координаты адреса')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
    ]
