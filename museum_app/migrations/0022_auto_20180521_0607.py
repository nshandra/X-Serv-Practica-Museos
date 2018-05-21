# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0021_auto_20180520_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='user',
            field=models.CharField(max_length=30, serialize=False, primary_key=True),
        ),
    ]
