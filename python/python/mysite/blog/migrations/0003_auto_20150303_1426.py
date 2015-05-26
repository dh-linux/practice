# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150303_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='ranking',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blog',
            name='view_count',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
