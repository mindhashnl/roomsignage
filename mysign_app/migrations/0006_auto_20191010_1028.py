# Generated by Django 2.2.5 on 2019-10-10 10:28

from django.db import migrations

import mysign_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('mysign_app', '0005_auto_20191003_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=mysign_app.models.CIEmailField(max_length=254, unique=True, verbose_name='email'),
        ),
    ]
