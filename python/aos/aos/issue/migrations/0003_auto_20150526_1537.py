# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0002_remove_product_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pline',
            field=models.CharField(unique=True, max_length=64),
            preserve_default=True,
        ),
    ]
