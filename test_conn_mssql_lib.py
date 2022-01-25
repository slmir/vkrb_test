"""import pyodbc


cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-6LJM1LE\MSSQLSERVERDPNEW;PORT=63405;DATABASE=VKRBTestBase;UID=mainadmin;PWD=Mir2020')
cursor = cnxn.cursor()

cnxn_system = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-6LJM1LE\MSSQLSERVERDPNEW;PORT=63405;DATABASE=VKRBSys;UID=mainadmin;PWD=Mir2020')
cursor_system = cnxn_system.cursor()

rows = cursor_system.execute("SELECT ID,Connection FROM Connect_dict where Active_connect = 1")
posts = [dict(id=row[0], conn_name=row[1]) for row in rows.fetchall()]"""

#print(posts)


import pymssql

conn = pymssql.connect(server='DESKTOP-6LJM1LE\MSSQLSERVERDPNEW', user='mainadmin', password='Mir2020', database='VKRBSys')
cursors = conn.cursor()

cursors.execute('SSELECT c1,c2 FROM table')
row = cursors.fetchone()
while row:
    print("c1=%d, c2=%s" % (row[0], row[1]))
    row = cursors.fetchone()

conn.close()