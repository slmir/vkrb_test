from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import nipyapi
from random import randrange
import time
import jaydebeapi
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
import urllib
import urllib.parse

app = Flask(__name__)
#nipyapi.config.nifi_config.host = 'http://localhost:8080/nifi-api'
#nipyapi.config.registry_config.host = 'http://localhost:18080/nifi-registry-api'
#root_id = nipyapi.canvas.get_root_pg_id()
#root_process_group = nipyapi.canvas.get_process_group(root_id, 'id')
#nipyapi.canvas.schedule_process_group(root_id, False)
app.debug = False
app.config['SECRET_KEY'] = 'dsfg12dfg14ds4fg54sd45f6g4654fds5g4ds12fg1d4g4dfg1sd2g1d32fg1ds2f3gsdfg'

#manager = Manager(app)
#app.config['SQLACHEMY_DATABASE_URI'] = 'mssql+pyodbc://root:pass@DESKTOP-6LJM1LE\MSSQLSERVERDPNEW/VKRBTestBase'
db = SQLAlchemy(app)


params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 10.0};SERVER=DESKTOP-6LJM1LE\MSSQLSERVERDPNEW;DATABASE=VKRBTestBase;UID=mainadmin;PWD=Mir2020")
#engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
# Data Source=DESKTOP-6LJM1LE\MSSQLSERVERDPNEW;Initial Catalog=VKRBTestBase;Integrated Security=True
# 'mssql+pyodbc://root:pass@localhost/my_db'"""


starttime=time.time()
DB_type = ''
Name_list = {"names_of_strings":"______"}


#создать класс в котором будет создаваться таблица с id и запясими -
#араметрами подключения - типом СУБД, тип схема, имя таблицы,
#озможно добавить массив с типом array -
# можно сделать выбор столбцом при помощи галочек и более детальная настройка-
# каждый столбец на своей строке и рядом место для написания запроса по этому столбцу

import pyodbc


cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-6LJM1LE\MSSQLSERVERDPNEW;PORT=63405;DATABASE=VKRBTestBase;UID=mainadmin;PWD=Mir2020')
cursor = cnxn.cursor()

cnxn_system = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-6LJM1LE\MSSQLSERVERDPNEW;PORT=63405;DATABASE=VKRBSys;UID=mainadmin;PWD=Mir2020')
cursor_system = cnxn_system.cursor()
i = 1
"""cursor.execute('select t1, t2 from test_table')
row=cursor.fetchone()

for row in cursor.execute('select t1, t2 from test_table'):
    print(row.t1, row.t2)



for row in cursor.execute('select t1, t2 from test_table'):
    print(row.t1, row.t2)"""

# for row in cursor.execute("""
 #                           select t1, t2
 #                           from test_table
#                            where t1>1"""):

 #   print("-----------------------\n",row.t1, row.t2, "\n")

#class Session_data(db.Model):
    

class ContactForm(FlaskForm):
    DB_type = StringField("Db_type: ", validators=[DataRequired()])
    DB_name = StringField("Db_name: ", validators=[DataRequired()])
    TB_name = TextAreaField("Table_name", validators=[DataRequired()])
    submit = SubmitField("Submit")


def stop_conn():
    global cursor
    cursor.close()
    del cursor


def write_attr(f1,f2,f3):
    global Name_list
    Name_list["DB_type"] = f1
    Name_list["DB_name"] = f2
    Name_list["TB_name"] = f3
    print(Name_list)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('main.html')


@app.route('/about')
def about():
    return 'About page'


@app.route('/connection_check', methods=['POST', 'GET'])
def connection_check():
    rows = cursor_system.execute("SELECT ID,Connection FROM Connect_dict where Active_connect = 1")
    posts = [dict(id=row[0], conn_name=row[1]) for row in rows.fetchall()]
    posts_table = []

    default_connection_string = "Выберите базу данных..."

    if 'column_select_submit' in request.form:
        counts = int(request.form.get('columns_count'))
        print(counts)
        list_column = {}
        columns_list = {}
        table_list=[]
        columns_idd=[]
        spisok = 'SELECT '
        cnt_def = counts
        #for i in count:
        #    rows = cursor_system.execute("SELECT TOP 1 ID,Column_name FROM Column_dict where ID='" + request.form.get('column_select'+i) + "'")
           # list_column.update(dict(id=row[0], table_name=row[1]) for row in rows.fetchall())
        for i in range(1, counts+1):
            col_i = request.form.get('column_select'+str(i)+'')
            print(col_i)
            list_column.update({str(i): col_i})
        print(list_column)
        list_col = [dict(id=key, col_name=list_column[key]) for key in list_column]

        k_count = 0
        columns = {}

        for key in list_column.keys():
            k_count += 1
            columns_idd.append(str(list_column[key]))
            rows_column = cursor_system.execute("SELECT Column_name FROM Column_dict where ID ='" + list_column[key] + "'")
            for row in rows_column.fetchall():
                row = str(row)[2:len(str(row)) - 4]
                columns_list.update({k_count:({list_column[key]:str(row)})})
                spisok = spisok + row + ', '


        #columns_list_dict = {}
        #columns_list_dict = [dict(id=key, col_name=list_column[key]) for key in list_column]


        """for key in columns_list.keys():
            k_count+=1
            columns_idd.append(key)
            #str_k=str(k)
            #spisok = spisok+str_k[2:len(str_k)-4]+', '
            columns_list[key] = columns_list[key][2:len(columns_list[key]) - 4]
            spisok = spisok + columns_list[key] + ', '
            columns.update({k_count:({key:columns_list[key]})})"""

        #for i, (k, v) in enumerate(columns_list.items()):
        #    print(i, type(i), k, type(k), v)


        ff11 = 'abc'

        spisok = spisok[0:len(spisok)-2]
        i=1
        for key in columns:
            print(key)
            if key==str(i):
                print('---', columns[key])
            i+=1

        print('columns: --- ', columns)
        print(list_col)
        connection_str = request.form.get('connection_str')
        table_name = request.form.get('table_select')
        row_def_con = cursor_system.execute("SELECT ID,Connection FROM Connect_dict where ID='" + connection_str + "'")
        posts_def_con = [dict(id=row[0], conn_name=row[1]) for row in row_def_con.fetchall()]
        rows = cursor_system.execute(
            "SELECT ID,Connection FROM Connect_dict where Active_connect = 1 and ID !='" + connection_str + "'")
        posts = [dict(id=row[0], conn_name=row[1]) for row in rows.fetchall()]
        row_def_con = cursor_system.execute("SELECT ID,Table_name FROM Table_dict where ID='" + table_name + "'")
        table_def_con = [dict(id=row[0], table_name=row[1]) for row in row_def_con.fetchall()]

        table_rows = cursor_system.execute("SELECT Table_name FROM Table_dict where ID ='" + table_name + "'")
        for row in table_rows.fetchall():
            table_list.append(row)

        for p in table_list:
            str_p = str(p)
            spisok = spisok+'\n'+'FROM '+ str_p[2:len(str_p)-4]

        rows = cursor_system.execute(
            "SELECT ID,Table_name FROM Table_dict where Active_table = 1 and ID !='" + table_name + "' and Connect_id='" + connection_str + "'")
        posts_table = [dict(id=row[0], table_name=row[1]) for row in rows.fetchall()]

        rows_column = cursor_system.execute(
            "SELECT ID,Column_name FROM Column_dict where Table_id ='" + table_name + "'")
        posts_column = [dict(id=str(row[0]), column_name=row[1]) for row in rows_column.fetchall()]



        return render_template('connection_check.html', posts=posts, tables=posts_table, columns=posts_column,
                               conn_def=posts_def_con, table_def=table_def_con, listing_column=list_col, sp=spisok, column_def=columns_list, count_def=cnt_def, columns_id=columns_idd,ff11=ff11)


    if 'conn_select' in request.form:
        spisok = ''
        connection_str = request.form.get('connection_str')
        row_def_con = cursor_system.execute("SELECT ID,Connection FROM Connect_dict where ID='" + connection_str + "'")
        posts_def_con = [dict(id=row[0], conn_name=row[1]) for row in row_def_con.fetchall()]
        rows = cursor_system.execute("SELECT ID,Connection FROM Connect_dict where Active_connect = 1 and ID !='" + connection_str + "'")
        posts = [dict(id=row[0], conn_name=row[1]) for row in rows.fetchall()]

        default_connection_string = connection_str
        default_table_string = "Выберите таблицу..."
        rows_table = cursor_system.execute("SELECT ID,Table_name FROM Table_dict where Active_table = 1 and Connect_id='"+connection_str+"'")
        posts_table = [dict(id=row[0], table_name=row[1]) for row in rows_table.fetchall()]
        return render_template('connection_check.html', posts=posts, tables=posts_table, conn_def=posts_def_con,sp=spisok, count_def=-1)

    """if 'conn_select' in request.form and request.method == 'POST':
        connection_str = request.form.get('connection_str')
        rows_table = cursor_system.execute("SELECT td.ID,td.Table_name FROM Table_dict td left join Connect_dict cd on cd.ID=td.Connect_id where td.Active_table = 1 and cd.Connection='"+connection_str+"'")
        posts_table = [dict(id=row[0], table_name=row[1]) for row in rows_table.fetchall()]
        return render_template('connection_check.html', posts=posts, tables=posts_table)"""


    """if 'connection_str' in request.form:
        connection_str = request.form.get('connection_str')
        rows_table = cursor_system.execute("SELECT td.ID,td.Table_name FROM Table_dict td left join Connect_dict cd on cd.ID=td.Connect_id where td.Active_table = 1 and cd.Connection='"+connection_str+"'")
        posts_table = [dict(id=row[0], table_name=row[1]) for row in rows_table.fetchall()]
        return render_template('connection_check.html', posts=posts, tables=posts_table, Def_conn=default_connection_string)
"""
    if 'table_select' in request.form:
        # метод выбора списка столбцов
        spisok = ''
        columns_idd=[]
        connection_str = request.form.get('connection_str')
        table_name = request.form.get('table_select')
        row_def_con = cursor_system.execute("SELECT ID,Connection FROM Connect_dict where ID='" + connection_str + "'")
        posts_def_con = [dict(id=row[0], conn_name=row[1]) for row in row_def_con.fetchall()]
        rows = cursor_system.execute("SELECT ID,Connection FROM Connect_dict where Active_connect = 1 and ID !='" + connection_str + "'")
        posts = [dict(id=row[0], conn_name=row[1]) for row in rows.fetchall()]
        row_def_con = cursor_system.execute("SELECT ID,Table_name FROM Table_dict where ID='" + table_name + "'")
        table_def_con = [dict(id=row[0], table_name=row[1]) for row in row_def_con.fetchall()]
        rows = cursor_system.execute("SELECT ID,Table_name FROM Table_dict where Active_table = 1 and ID !='" + table_name + "' and Connect_id='" + connection_str + "'")
        posts_table = [dict(id=row[0], table_name=row[1]) for row in rows.fetchall()]

        rows_column = cursor_system.execute("SELECT ID,Column_name FROM Column_dict where Table_id ='"+table_name+"'")
        posts_column = [dict(id=row[0], column_name=row[1]) for row in rows_column.fetchall()]
        return render_template('connection_check.html', posts=posts, tables=posts_table, columns=posts_column,sp=spisok, conn_def=posts_def_con, table_def=table_def_con, count_def=-1, columns_id=columns_idd)



    if request.method == 'POST' and not 'conn_select' and not 'column_select_submit':
        columns_idd=[]
        connection_str = request.form.get('connection_str')
        user_login = request.form.get('login_str')
        user_pswrd = request.form.get('password_str')
        #nipyapi.canvas.update_variable_registry(root_process_group, ([('Connection_str', connection_str)]))
        #nipyapi.canvas.update_variable_registry(root_process_group, ([('user_login', user_login)]))
        #nipyapi.canvas.update_variable_registry(root_process_group, ([('user_password', user_pswrd)]))

        time.sleep(2 - ((time.time() - starttime) % 2))
        cursor.execute("INSERT INTO test_table(t1, t2) VALUES (999, '"+connection_str+"')")
        #cursor.execute("INSERT INTO test_table(t1, t2) VALUES (103, '" + user_login + "')")
        #cursor.execute("INSERT INTO test_table(t1, t2) VALUES (103, '" + user_pswrd + "')")
        """cursor.execute('select t1, t2 from test_table')
        row = cursor.fetchone()"""
        cnxn.commit()
        return redirect('/nifi')
    return render_template('connection_check.html', posts=posts, tables=posts_table, Def_conn=default_connection_string, count_def=-1)
    #return render_template('tre_razdel.html')


@app.route('/query_result', methods=['POST', 'GET'])
def query_result():
    connection_str = request.form.get('connection_str')
    table_name = request.form.get('table_select')


    print(connection_str, ' - ', table_name)

    row_def_con = cursor_system.execute("SELECT ID,Connection FROM Connect_dict where ID='" + connection_str + "'")
    posts_def_con = [dict(id=row[0], conn_name=row[1]) for row in row_def_con.fetchall()]
    rows = cursor_system.execute(
        "SELECT ID,Connection FROM Connect_dict where Active_connect = 1 and ID !='" + connection_str + "'")
    posts = [dict(id=row[0], conn_name=row[1]) for row in rows.fetchall()]
    row_def_con = cursor_system.execute("SELECT ID,Table_name FROM Table_dict where ID='" + table_name + "'")
    table_def_con = [dict(id=row[0], table_name=row[1]) for row in row_def_con.fetchall()]
    rows = cursor_system.execute(
        "SELECT ID,Table_name FROM Table_dict where Active_table = 1 and ID !='" + table_name + "' and Connect_id='" + connection_str + "'")
    posts_table = [dict(id=row[0], table_name=row[1]) for row in rows.fetchall()]

    rows_column = cursor_system.execute(
        "SELECT ID,Column_name FROM Column_dict where Table_id ='" + table_name + "'")
    posts_column = [dict(id=row[0], column_name=row[1]) for row in rows_column.fetchall()]
    list_col = {}

    if 'column_select_submit' in request.form:
        list_column = {'1':'empty'}
        print('list_column --- ',list_column)
        list_col = [dict(id=row[0], col_name=row[1]) for row in list_column]
        
        counts = int(str(request.form.get('columns_count')))
        print('counts - ', counts)
        list_column = {}
        # for i in count:
        #    rows = cursor_system.execute("SELECT TOP 1 ID,Column_name FROM Column_dict where ID='" + request.form.get('column_select'+i) + "'")
        # list_column.update(dict(id=row[0], table_name=row[1]) for row in rows.fetchall())
        for i in range(counts):
            col_i = request.form.get('column_select' + str(i) + '')
            print('col_i - ', col_i)
            list_column.update({str(i): col_i})
            print('list_column - ', list_column)
        list_col = [dict(id=row[0], col_name=row[1]) for row in list_column]
        print('list_col - ', list_col)
        return render_template('connection_check1.html', posts=posts, tables=posts_table, columns=posts_column,
                           conn_def=posts_def_con, table_def=table_def_con, listing_column=list_col)

    return render_template('connection_check.html', posts=posts, tables=posts_table, columns=posts_column,
                           conn_def=posts_def_con, table_def=table_def_con, listing_column=list_col)




@app.route('/nifi', methods=['POST', 'GET'])
def nifi():
    if request.method == 'POST':
        """if 'button_conn' in request.form:
            connection_str = request.form.get('connection_str')
            nipyapi.canvas.update_variable_registry(root_process_group, ([('Connection_str', str(connection_str))]))
            time.sleep(2 - ((time.time() - starttime) % 2))
            cursor.execute("INSERT INTO test_table(t1, t2) VALUES (25, 'Значение из nifi')")
            return render_template('go_to_nifi.html')"""

        if 'submit_button_nifi' in request.form:
            stop_conn()
            time.sleep(2 - ((time.time() - starttime) % 2))
            #nipyapi.canvas.schedule_process_group(root_id, True)
            time.sleep(2 - ((time.time() - starttime) % 2))
            nipyapi.canvas.schedule_process_group('6a7c4e77-017c-1000-5c29-b5322213bd7d', False)
            """while nipyapi.canvas.get_process_group_status('017c100b-ee54-138e-cb41-7a1d45803b1c', 'names') == '':
                time.sleep(2 - ((time.time() - starttime) % 2))
            else:
                nipyapi.canvas.schedule_process_group(root_id, False)"""
            #cnxn.close()
            return redirect('/close_conn')
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!DB_type = request.form.get('db_type')
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!cursor.execute("INSERT INTO test_table(t1, t2) VALUES (16, 'TYPE:"+DB_type+"')")


        #return connection_str
        #nipyapi.canvas.get_process_group_status('017c100b-ee54-138e-cb41-7a1d45803b1c', 'names')

    return render_template('go_to_nifi.html')


@app.route('/close_conn', methods=['POST', 'GET'])
def closeconn():
    if request.method == 'POST':
        if 'close_conn_button' in request.form:
            cnxn.close()
    return render_template('close_conn.html')


@app.route('/params', methods=['POST', 'GET'])
def params():
    #form = ContactForm()
    if request.method == 'POST':
        """nipyapi.canvas.schedule_process_group(root_id, False)
        DB_type = request.form.get('dbtype')
        nipyapi.canvas.update_variable_registry(root_process_group, ([('test1', DB_type)]))
        DB_name = request.form['dbname']
        nipyapi.canvas.update_variable_registry(root_process_group, ([('test1', DB_name)]))
        TB_name = request.form['tablename']
        cursor.execute("INSERT INTO test_table(t1, t2) VALUES (4, {0})".format(DB_type))
        cursor.execute("INSERT INTO test_table(t1, t2) VALUES (5, {0})".format(DB_name))
        cursor.execute("INSERT INTO test_table(t1, t2) VALUES (6, {0})".format(TB_name))
        cnxn.commit()"""


        #DB_type = form.DB_type.data
        #DB_name = form.DB_name.data
        #TB_name = form.TB_name.data
        DB_type = request.form.get('DB_type')
        cursor.execute("INSERT INTO test_table(t1, t2) VALUES (16, 'TYPE:" + DB_type + "')")
        #cursor.execute("INSERT INTO test_table(t1, t2) VALUES (5, {0})".format(DB_name))
        #cursor.execute("INSERT INTO test_table(t1, t2) VALUES (6, {0})".format(TB_name))
        cnxn.commit()
        return redirect(url_for('params'))
    return render_template('params.html')



if __name__ == "__main__":
    app.run(debug=True)