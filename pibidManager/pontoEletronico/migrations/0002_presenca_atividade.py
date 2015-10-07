# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pontoEletronico', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='presenca',
            name='atividade',
            field=models.TextField(null=True, verbose_name=b'Atividade'),
        ),
    ]
