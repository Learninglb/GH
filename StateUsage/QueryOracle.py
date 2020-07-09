import cx_Oracle
db = cx_Oracle.connect('SPWebProg', 'To the other side 14','fecsql03/darden_dev_blasing')
print(db.version)