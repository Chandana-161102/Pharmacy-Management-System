from cgitb import text
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import csv
import secret

app = Flask(__name__)
app.config['MYSQL_HOST'] = secret.passHidden['HOST']
app.config['MYSQL_USER'] = secret.passHidden['DATABASE_USER']
app.config['MYSQL_PASSWORD']=secret.passHidden['DATABASE_PASSWORD']
app.config['MYSQL_DB'] = secret.passHidden['DATABASE']

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    cur = mysql.connection.cursor()
    views = cur.execute("SHOW TABLES")

    if views > 0 :
        viewdetails = cur.fetchall()
        return render_template('view.html',viewdetails=viewdetails)

@app.route('/update')
def update():
    cur = mysql.connection.cursor()
    views = cur.execute("SHOW TABLES")

    if views > 0 :
        viewdetails = cur.fetchall()
        return render_template('update.html',viewdetails=viewdetails)

@app.route('/import')
def import_table():
    cur = mysql.connection.cursor()
    views = cur.execute("SHOW TABLES")

    if views > 0 :
        viewdetails = cur.fetchall()
        return render_template('import.html',viewdetails=viewdetails)

@app.route('/export')
def export_table():
    cur = mysql.connection.cursor()
    views = cur.execute("SHOW TABLES")

    if views > 0 :
        viewdetails = cur.fetchall()
        return render_template('export.html',viewdetails=viewdetails)

@app.route('/export/<table>',methods=['GET','POST'])
def table_export(table):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # command = "SELECT * FROM "+table+" INTO OUTFILE '/tmp/"+table+".csv' FIELDS ENCLOSED BY '\"' TERMINATED BY ',' ESCAPED BY '\"' LINES TERMINATED BY '\\r\\n'"
        file = open('export_files/'+table+'.csv','w')
        writer=csv.writer(file)
        views = cur.execute("SELECT * FROM "+table)
        if views > 0 :
            viewdetails = cur.fetchall()
            for row in viewdetails:
                writer.writerow(row)
            file.close()
            return render_template('index.html')

@app.route('/import/<table>',methods=['GET','POST'])
def table_import(table):
    cur = mysql.connection.cursor()
    cur.execute("SHOW columns FROM "+table)
    columname = cur.fetchall() 
    if request.method == 'POST':
        file = open(request.form['file'])
        csvreader = csv.reader(file)
        command="INSERT INTO "+table+" VALUES "
        for row in csvreader:
            command+="("
            for i in range(len(row)):
                if columname[i][1]!='int':
                    command+="'"+row[i]+"'"
                else:
                    command+=row[i]
                if i!=len(row)-1:
                    command+=","
            command+=")"
            command+=","
        fincommand = command[0:len(command)-1]
        print(fincommand)
        file.close()
        cur = mysql.connection.cursor()
        cur.execute(fincommand)
        mysql.connection.commit()
        return render_template('index.html')

@app.route('/view/<table>',methods=['GET','POST'])
def table_display(table):
    cur = mysql.connection.cursor()
    cur.execute("SHOW columns FROM "+table)
    columname = cur.fetchall() 
    views = cur.execute("SELECT * FROM "+table)
    if views > 0 :
        viewdetails = cur.fetchall()
        return render_template('table.html',viewdetails=viewdetails,columndetails=columname,tableName=table)

@app.route('/update/<table>',methods=['GET','POST'])
def display(table):
    cur = mysql.connection.cursor()
    cur.execute("SHOW columns FROM "+table)
    columname = cur.fetchall() 
    views = cur.execute("SELECT * FROM "+table)
    if views > 0 :
        viewdetails = cur.fetchall()
        return render_template('updatetable.html',viewdetails=viewdetails,columndetails=columname,tableName=table)


@app.route('/update_table/<table>/<column>/<type>/<value>',methods=['GET','POST'])
def table_update(table,column,type,value):
    cur = mysql.connection.cursor()
    cur.execute("SHOW columns FROM "+table)
    columname = cur.fetchall() 
    if request.method == 'POST':
        if type!='int':
            command = "UPDATE "+table+" SET "+ column+"='"+request.form[column]+"' WHERE "+column+"='"+value+"'";    
        else:
            command = "UPDATE "+table+" SET "+column+"="+request.form[column]+" WHERE "+column+"="+value;
        cur = mysql.connection.cursor()
        cur.execute(command)
        mysql.connection.commit()
    views = cur.execute("SELECT * FROM "+table)
    if views > 0 :
        viewdetails = cur.fetchall()
        return render_template('updatetable.html',viewdetails=viewdetails,columndetails=columname,tableName=table)

@app.route('/get_data/<table>',methods=['GET','POST'])
def post_data(table):
    cur = mysql.connection.cursor()
    cur.execute("SHOW columns FROM "+table)
    columname = cur.fetchall() 
    if request.method == 'POST':
        command = "INSERT INTO "+table+" VALUES (";
        for column in columname:
            if column[1]!='int':
                command+="'"+request.form[column[0]]+"',"    
            else:
                command+=request.form[column[0]]+","
        fincommand = command[0:len(command)-1]
        fincommand+=")"
        print(fincommand)
        cur = mysql.connection.cursor()
        cur.execute(fincommand)
        mysql.connection.commit()
        views = cur.execute("SELECT * FROM "+table)
        if views > 0 :
            viewdetails = cur.fetchall()
            return render_template('table.html',viewdetails=viewdetails,columndetails=columname,tableName=table)

@app.route('/del_data/<table>',methods=['GET','POST'])
def delete_data(table):
    cur = mysql.connection.cursor()
    cur.execute("SHOW columns FROM "+table)
    columname = cur.fetchall() 
    if request.method == 'POST':
        command = "DELETE FROM "+table+" WHERE "+columname[0][0]+"="+request.form['id']
        print(command)
        cur = mysql.connection.cursor()
        cur.execute(command)
        mysql.connection.commit()
        views = cur.execute("SELECT * FROM "+table)
        if views > 0 :
            viewdetails = cur.fetchall()
            return render_template('table.html',viewdetails=viewdetails,columndetails=columname,tableName=table)

if __name__ == "__main__":
    app.run(debug=True)