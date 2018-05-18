# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0015_auto_20180518_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='css_page',
            field=models.TextField(blank=True),
        ),
    ]
