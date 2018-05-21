# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0020_auto_20180520_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museum',
            name='email',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='museum',
            name='tel',
            field=models.CharField(max_length=240, blank=True),
        ),
    ]
