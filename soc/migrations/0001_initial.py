# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='um_ecomm_dept_units_rept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_yr', models.CharField(db_column=b'fiscal_yr', max_length=4)),
                ('calendar_yr', models.CharField(db_column=b'calendar_yr', max_length=4)),
                ('month', models.CharField(db_column=b'month', max_length=2)),
                ('deptid', models.CharField(db_column=b'deptid', max_length=6)),
                ('dept_descr', models.CharField(db_column=b'dept_descr', max_length=30)),
                ('dept_grp', models.CharField(db_column=b'dept_grp', max_length=20)),
                ('dept_grp_desc', models.CharField(db_column=b'dept_grp_desc', max_length=30)),
                ('dept_grp_vp_area', models.CharField(db_column=b'dept_grp_vp_area', max_length=20)),
                ('dept_grp_vp_area_descr', models.CharField(db_column=b'dept_grp_vp_area_descr', max_length=30)),
                ('account', models.CharField(db_column=b'account', max_length=6)),
                ('account_desc', models.CharField(db_column=b'account_desc', max_length=20)),
                ('charge_group', models.CharField(db_column=b'charge_group', max_length=50)),
                ('charge_code', models.CharField(db_column=b'charge_code', max_length=12)),
                ('description', models.CharField(db_column=b'description', max_length=50)),
                ('unit_rate', models.CharField(db_column=b'unit_rate', max_length=40)),
                ('quantity', models.FloatField()),
                ('amount', models.FloatField()),
                ('dept_bud_seq', models.CharField(db_column=b'dept_bud_seq', max_length=20)),
                ('dept_bud_seq_descr', models.CharField(db_column=b'dept_bud_seq_descr', max_length=30)),
            ],
            options={
                'abstract': False,
                'db_table': '"PINN_CUSTOM"."UM_ECOMM_DEPT_UNITS_REPT"',
                'managed': False,
            },
        ),
    ]