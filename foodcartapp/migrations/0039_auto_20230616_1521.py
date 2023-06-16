# Generated by Django 3.2.15 on 2023-06-16 15:21

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_auto_20230616_1308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='surname',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='orderproduct',
            old_name='count',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.AddField(
            model_name='order',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(default='', max_length=128, region=None, verbose_name='Телефон'),
            preserve_default=False,
        ),
    ]
