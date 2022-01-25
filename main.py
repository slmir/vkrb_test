import jaydebeapi
import pyodbc


column_list={}
column_list.update({'1':({'1':'one'})})
column_list.update({'12':({'12':'two'})})
column_list.update({'123':({'223':'free'})})
column_list.update({'1244':({'455':'four'})})


for i in column_list:
    for key in column_list[i]:
        print(i,'----',key,'----',column_list[i][key])

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-6LJM1LE\MSSQLSERVERDPNEW;PORT=1433;DATABASE=VKRBTestBase;UID=sa;PWD=Mirsonov2020')
cursor = cnxn.cursor()

cursor.execute('select t1, t2 from test_table')
row=cursor.fetchone()

for row in cursor.execute('select t1, t2 from test_table'):
    print(row.t1, row.t2)

strl = '123456'
cursor.execute("INSERT INTO test_table(t1, t2) VALUES (3,'" + strl + "')")

for row in cursor.execute('select t1, t2 from test_table'):
    print(row.t1, row.t2)

for row in cursor.execute("""
                            select t1, t2 
                            from test_table
                            where t1>1"""):

    print("-----------------------\n",row.t1, row.t2, "\n")

cnxn.commit()