# Generated by Django 2.1.7 on 2019-11-11 03:26

from django.db import migrations

import core.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='txid',
            field=core.model_fields.HexField(max_length=64),
        ),
    ]