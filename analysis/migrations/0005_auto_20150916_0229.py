# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0004_auto_20150915_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysissample',
            name='condition',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
