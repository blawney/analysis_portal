# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_analysis_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='finish_time',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
    ]
