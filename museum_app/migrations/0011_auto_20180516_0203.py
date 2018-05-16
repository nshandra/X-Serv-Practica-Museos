# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0010_auto_20180516_0159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='id',
        ),
        migrations.AlterField(
            model_name='collection',
            name='user',
            field=models.CharField(max_length=60, serialize=False, primary_key=True),
        ),
    ]
