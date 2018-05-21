# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0018_auto_20180518_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='museum',
            name='votes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
