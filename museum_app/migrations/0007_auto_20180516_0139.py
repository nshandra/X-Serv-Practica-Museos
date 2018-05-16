# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0006_auto_20180516_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='css_page',
            field=models.TextField(default='', blank=True),
        ),
    ]
