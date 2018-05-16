# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0011_auto_20180516_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='css_page',
            field=models.TextField(default=''),
        ),
    ]
