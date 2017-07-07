# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 11:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('d3_primeri', '0002_auto_20170527_1338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='node',
        ),
        migrations.RemoveField(
            model_name='link',
            name='node',
        ),
        migrations.AddField(
            model_name='link',
            name='child_node',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='child_node', to='d3_primeri.Node'),
        ),
        migrations.AddField(
            model_name='link',
            name='parent_node',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='parent_node', to='d3_primeri.Node'),
        ),
        migrations.AddField(
            model_name='node',
            name='attributes',
            field=models.ManyToManyField(to='d3_primeri.Attribute'),
        ),
    ]
