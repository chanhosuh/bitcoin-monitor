# Generated by Django 2.1.7 on 2019-11-10 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='id',
        ),
        migrations.AlterField(
            model_name='block',
            name='height',
            field=models.PositiveIntegerField(help_text='zero-index block height; primary key', primary_key=True, serialize=False),
        ),
    ]
