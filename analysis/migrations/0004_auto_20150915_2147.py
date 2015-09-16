# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0003_auto_20150915_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('condition', models.CharField(max_length=50)),
                ('is_used', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnalysisSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.CharField(max_length=1200)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('finish_time', models.DateTimeField(default=None, null=True, blank=True)),
                ('result_url', models.URLField()),
                ('is_complete', models.BooleanField(default=False)),
                ('has_error', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BaseSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('project', models.ForeignKey(to='analysis.Project')),
            ],
        ),
        migrations.RemoveField(
            model_name='sample',
            name='project',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='command',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='finish_time',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='has_error',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='is_complete',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='result_url',
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='start_time',
        ),
        migrations.AddField(
            model_name='analysis',
            name='common_name',
            field=models.CharField(default=None, max_length=100, blank=True),
        ),
        migrations.DeleteModel(
            name='Sample',
        ),
        migrations.AddField(
            model_name='analysissummary',
            name='analysis',
            field=models.ForeignKey(to='analysis.Analysis'),
        ),
        migrations.AddField(
            model_name='analysissample',
            name='analysis',
            field=models.ForeignKey(to='analysis.Analysis'),
        ),
        migrations.AddField(
            model_name='analysissample',
            name='sample',
            field=models.ForeignKey(to='analysis.BaseSample'),
        ),
    ]
