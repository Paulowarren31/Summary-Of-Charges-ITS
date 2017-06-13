import cx_Oracle

connection_string = 'paulowar/Pw6517nP@pinntst.dsc.umich.edu:1521/pinndev.world'

conn = cx_Oracle.connect(connection_string)
cursor = conn.cursor()

query = "select * from um_ecomm_dept_units_rept where deptid='926200' and month BETWEEN 06 and 12 and calendar_yr between 2015 and 2016"

vp_area = cursor.execute(query).fetchall()

for v in  vp_area:
  print v

conn.close()

