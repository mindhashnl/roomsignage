# Generated by Django 2.2.5 on 2019-10-10 16:03

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysign_app', '0006_auto_20191010_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='text_color',
            field=colorfield.fields.ColorField(blank=True, default='#ffffff', max_length=18),
        ),
    ]
