# Generated by Django 2.1.7 on 2019-06-05 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20190605_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='locktime',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='version',
            field=models.BigIntegerField(help_text='only version 1 valid in Bitcoin Core'),
        ),
    ]
