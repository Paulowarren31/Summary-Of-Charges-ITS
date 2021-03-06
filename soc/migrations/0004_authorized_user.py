# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-03 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc', '0003_auto_20170803_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authorized_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deptid', models.CharField(db_column=b'deptid', max_length=10)),
                ('uniqname', models.CharField(db_column=b'uniqname', max_length=20)),
                ('role', models.CharField(db_column=b'role', max_length=30)),
                ('timestamp', models.DateField(db_column=b'timestamp')),
            ],
            options={
                'abstract': False,
                'db_table': 'PINN_CUSTOM"."UM_AUTHORIZED_DEPT_USERS',
                'managed': False,
            },
        ),
    ]
