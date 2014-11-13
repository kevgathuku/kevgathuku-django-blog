# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20141113_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='subtitle',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
