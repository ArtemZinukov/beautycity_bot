# Generated by Django 5.0.7 on 2024-07-25 15:49

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_client_phone_alter_registration_salon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=12, region=None, verbose_name='Номер телефона'),
        ),
    ]