# Generated by Django 2.1 on 2018-09-10 05:39

import core.model_fields
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('hash', core.model_fields.HexField(help_text='block hash in hex (32 bytes)', max_length=64, unique=True)),
                ('confirmations', models.IntegerField()),
                ('size', models.IntegerField()),
                ('stripped_size', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('height', models.PositiveIntegerField()),
                ('version', models.PositiveIntegerField()),
                ('merkle_root', core.model_fields.HexField(max_length=64)),
                ('time', models.PositiveIntegerField()),
                ('median_time', models.PositiveIntegerField()),
                ('nonce', models.PositiveIntegerField()),
                ('bits', core.model_fields.HexField(max_length=8)),
                ('difficulty', models.DecimalField(decimal_places=10, max_digits=20)),
                ('number_of_transactions', models.PositiveIntegerField()),
                ('previous_block_hash', core.model_fields.HexField(max_length=64)),
                ('next_block_hash', core.model_fields.HexField(max_length=64, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]