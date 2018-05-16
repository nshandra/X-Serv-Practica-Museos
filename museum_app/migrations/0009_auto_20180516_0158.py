# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0008_auto_20180516_0148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='added_museum',
            name='museum',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='museums',
        ),
    ]
