# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bolsista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=11)),
                ('user', models.OneToOneField(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Frequencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mes', models.SmallIntegerField()),
                ('ano', models.SmallIntegerField()),
                ('atualizacao', models.DateTimeField(auto_now=True)),
                ('bolsista', models.ForeignKey(to='pontoEletronico.Bolsista')),
            ],
        ),
        migrations.CreateModel(
            name='Presenca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField(default=django.utils.timezone.now)),
                ('chegada', models.TimeField()),
                ('saida', models.TimeField(null=True)),
                ('atualizacao', models.DateTimeField(auto_now=True)),
                ('bolsista', models.ForeignKey(to='pontoEletronico.Bolsista')),
                ('frequencia', models.ForeignKey(to='pontoEletronico.Frequencia')),
            ],
        ),
    ]
