# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0003_auto_20150526_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pline',
            field=models.CharField(max_length=64),
            preserve_default=True,
        ),
    ]
