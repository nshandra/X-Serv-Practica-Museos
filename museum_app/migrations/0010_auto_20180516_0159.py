# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0009_auto_20180516_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='added_museum',
            name='collection',
            field=models.ForeignKey(to='museum_app.Collection', null=True),
        ),
        migrations.AddField(
            model_name='added_museum',
            name='museum',
            field=models.ForeignKey(to='museum_app.Museum', null=True),
        ),
    ]
