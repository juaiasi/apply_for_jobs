# Generated by Django 4.0.4 on 2022-05-23 01:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security_app', '0002_sharer_password_alter_sharer_limit_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharer',
            name='limit_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 29, 22, 50, 9, 732891)),
        ),
    ]
