# Generated by Django 5.0.7 on 2024-07-28 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_alter_registration_service_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='service_date',
            field=models.DateField(verbose_name='Дата процедуры'),
        ),
    ]