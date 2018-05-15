# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='museum',
        ),
        migrations.AddField(
            model_name='collection',
            name='css_page',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='museum',
            name='coment',
            field=models.ManyToManyField(to='museum_app.Comment'),
        ),
    ]
