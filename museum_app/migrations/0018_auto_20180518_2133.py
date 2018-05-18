# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0017_auto_20180518_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='added_museum',
            name='collection',
            field=models.ForeignKey(to='museum_app.Collection'),
        ),
        migrations.AlterField(
            model_name='added_museum',
            name='museum',
            field=models.ForeignKey(to='museum_app.Museum'),
        ),
    ]
