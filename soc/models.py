from django.db import models

# Create your models here.


class ExternalModel(models.Model):
  class Meta:
    managed = False
    abstract = True

class um_ecomm_dept_units_rept(ExternalModel):
  fiscal_yr = models.CharField(primary_key=True, db_column='fiscal_yr', max_length=4)
  calendar_yr = models.CharField(db_column='calendar_yr', max_length=4)
  month = models.CharField(db_column='month', max_length=2)
  deptid = models.CharField(db_column='deptid', max_length=6)
  dept_descr = models.CharField(db_column='dept_descr', max_length=30)
  dept_grp = models.CharField(db_column='dept_grp', max_length=20)
  dept_grp_descr = models.CharField(db_column='dept_grp_descr', max_length=30)
  dept_grp_vp_area = models.CharField(db_column='dept_grp_vp_area', max_length=20)
  dept_grp_vp_area_descr = models.CharField(db_column='dept_grp_vp_area_descr', max_length=30)
  account = models.CharField(db_column='account', max_length=6)
  account_desc = models.CharField(db_column='account_desc', max_length=20)
  charge_group = models.CharField(db_column='charge_group', max_length=50)
  charge_code = models.CharField(db_column='charge_code', max_length=12)
  description = models.CharField(db_column='description', max_length=50)
  # price per unit
  unit_rate = models.CharField(db_column='unit_rate', max_length=40)
  # number sold
  quantity = models.FloatField()
  # $$ made
  amount = models.FloatField()
  dept_bud_seq = models.CharField(db_column='dept_bud_seq', max_length=20)
  dept_bud_seq_descr = models.CharField(db_column='dept_bud_seq_descr', max_length=30)

  def __str__(self):
    return 'ACC: '+ self.account + ' GRP: ' + self.charge_group + ' DESCR: ' + self.description

  class Meta(ExternalModel.Meta):
    db_table = 'PINN_CUSTOM\".\"UM_ECOMM_DEPT_UNITS_REPT'
    ordering = ['account', 'charge_group', 'description']

class Search(models.Model):
  dept = models.CharField(max_length=15)
  time = models.CharField(max_length=15)

#any reads to a DB are send to the sqlite DB, 
#unless it is um_ecomm_dept_units_rept
class DBRouter(object):
  def db_for_read(self, model, **hints):
    if model._meta.db_table == 'PINN_CUSTOM"."UM_ECOMM_DEPT_UNITS_REPT':
      return 'oracle'
    return 'default'

  def db_for_write(self, model, **hints):
    return 'default'

