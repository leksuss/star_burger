# Generated by Django 3.2.15 on 2023-06-21 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_auto_20230620_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Необработанный'), (1, 'Собирается'), (2, 'Доставляется'), (3, 'Выполнен')], db_index=True, default=0, verbose_name='Статус'),
        ),
    ]
