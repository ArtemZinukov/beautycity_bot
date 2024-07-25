# Generated by Django 5.0.7 on 2024-07-25 07:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(max_length=100)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.master', verbose_name='Мастер')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_registration', models.DateTimeField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.client', verbose_name='Клиент')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.master', verbose_name='Мастер')),
                ('salon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.salon', verbose_name='Услуга')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.service', verbose_name='Услуга')),
            ],
        ),
        migrations.AddField(
            model_name='master',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.service', verbose_name='Услуга'),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
