# Generated by Django 2.1 on 2019-02-24 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='nonce',
            field=models.BigIntegerField(),
        ),
    ]