# Generated by Django 4.0.4 on 2022-05-23 01:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharer',
            name='password',
            field=models.CharField(blank=True, default='...', max_length=128),
        ),
        migrations.AlterField(
            model_name='sharer',
            name='limit_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 29, 22, 46, 8, 223198)),
        ),
    ]
