# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum_app', '0019_museum_votes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='museum',
            old_name='votes',
            new_name='vote',
        ),
    ]
