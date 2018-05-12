# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Added_Museum',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('user', models.CharField(max_length=60)),
                ('title', models.CharField(max_length=120)),
                ('museums', models.ManyToManyField(to='museum_app.Added_Museum')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Museum',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=240)),
                ('url', models.URLField(max_length=2048)),
                ('description', models.TextField()),
                ('access', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=440)),
                ('district', models.CharField(max_length=40)),
                ('tel', models.CharField(max_length=240)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='museum',
            field=models.ForeignKey(to='museum_app.Museum'),
        ),
        migrations.AddField(
            model_name='added_museum',
            name='museum',
            field=models.ForeignKey(to='museum_app.Museum'),
        ),
    ]
