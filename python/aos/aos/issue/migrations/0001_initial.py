# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('pline', models.CharField(max_length=64)),
                ('svn_path', models.CharField(max_length=256)),
                ('rsync_path', models.CharField(max_length=256)),
                ('port', models.IntegerField()),
                ('model', models.CharField(max_length=64)),
                ('test', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='rt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rt_id', models.IntegerField()),
                ('rt_title', models.CharField(max_length=256)),
                ('rt_content', models.TextField()),
                ('rt_status', models.CharField(max_length=64)),
                ('rt_lock', models.BooleanField(default=False)),
                ('product_name', models.ForeignKey(to='issue.product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
