# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0016_auto_20180518_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museum',
            name='coment',
            field=models.ManyToManyField(blank=True, to='museum_app.Comment'),
        ),
    ]
