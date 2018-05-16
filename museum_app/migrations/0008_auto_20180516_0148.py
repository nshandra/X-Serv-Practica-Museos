# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0007_auto_20180516_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='added_museum',
            name='added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
