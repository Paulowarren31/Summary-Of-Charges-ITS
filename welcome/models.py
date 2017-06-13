from django.db import models

# Create your models here.

#
#class ExternalModel(models.Model):
#
#  class Meta:
#    managed = False
#    abstract = True
#
#class Report(ExternalModel):
#  fiscal_yr = models.TextField(db_column='fiscal_yr', max_length=4)
#  calendar_yr = models.TextField(db_column='calendar_yr', max_length=4)
#  month = models.TextField(db_column='month', max_length=2)
#  deptid = models.TextField(db_column='deptid', max_length=4)
#  dept_descr = models.TextField(db_column='dept_descr', max_length=4)
#  dept_grp = models.TextField(db_column='dept_grp', max_length=4)
#  dept_grp_desc = models.TextField(db_column='dept_grp_desc', max_length=4)
#  dept_grp_vp_area = models.TextField(db_column='dept_grp_vp_area', max_length=4)
#  account = models.TextField(db_column='account', max_length=4)
#  account_desc = models.TextField(db_column='account_desc', max_length=4)
#  charge_group = models.TextField(db_column='charge_group', max_length=4)
#  charge_code = models.TextField(db_column='charge_code', max_length=4)
#  description = models.TextField(db_column='description', max_length=4)
#  unit_rate = models.TextField(db_column='unit_rate', max_length=4)
#  quantity = models.TextField(db_column='quantity', max_length=4)
#  amount = models.TextField(db_column='amount', max_length=4)
#  dept_bud_seq = models.TextField(db_column='dept_bud_seq', max_length=4)
#  dept_bud_seq_descr = models.TextField(db_column='dept_bud_seq_descr', max_length=4)
#
#  class Meta(ExternalModel.Meta):
#    db_table = '"PINN_CUSTOM"."UM_ECOMM_DEPT_UNITS_REPT"'
#    managed = False
