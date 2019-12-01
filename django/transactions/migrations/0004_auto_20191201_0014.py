# Generated by Django 2.2 on 2019-12-01 00:14

import django.contrib.postgres.fields
from django.db import migrations

import core.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0003_witness"),
    ]

    operations = [
        migrations.AddField(
            model_name="transactioninput",
            name="witness",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=core.model_fields.HexField(max_length=20000),
                null=True,
                size=None,
            ),
        ),
        migrations.DeleteModel(name="Witness",),
    ]