from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db

app = Flask(__name__)

dsn_hostname = "ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
dsn_uid = "ztg96113"
dsn_pwd = "AfS01sncyWGSzIEr"
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_port = "31505"
dsn_security = "SSL"
dsn = ("DRIVER={0};"
"DATABASE={1};"
"HOSTNAME={2};"
"PORT={3};"
"UID={4};"
"PWD={5};"
"SECURITY={6};").format(dsn_driver,dsn_database,dsn_hostname,dsn_port,dsn_uid,dsn_pwd,dsn_security)
print(dsn)
try:
  conn = ibm_db.pconnect(dsn,"","")
  print("success")
except:
  print(ibm_db.conn_errormsg())

@app.route("/" , methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    sql_stmt = "insert into USERTBL values(?,?,?,?,?)"
    stmt = ibm_db.prepare(conn, sql_stmt)
    username = request.form['username']
    password = request.form['password']
    phnnumber = request.form['phnnumber']
    bloodgroup = request.form['bloodgroup']
    email = request.form['email']
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.bind_param(stmt, 3, phnnumber)
    ibm_db.bind_param(stmt, 4, bloodgroup)
    ibm_db.bind_param(stmt, 5, email)
    
    try:
      ibm_db.execute(stmt)
      return redirect('/index')
    except:
      print(ibm_db.stmt_errormsg())

  return render_template('landing.html')


@app.route("/login",methods=('GET','POST'))
def loginpage():
    if request.method == 'POST':
      
      if request.form['action'] == 'DONOR':
        username = request.form['username']
        password = request.form['password']
        query = "select COUNT(*) from usertbl where username='"+username+"' and password='"+password+"'"
        stmt5 = ibm_db.exec_immediate(conn,query)
        row = ibm_db.fetch_tuple(stmt5)
        if(row[0] ==1 ):
            return redirect("/donordetails")
        return render_template("/index")

      if request.form['action'] == 'RECEIVER':
        username = request.form['username']
        password = request.form['password']
        query = "select COUNT(*) from usertbl where username='"+username+"' and password='"+password+"'"
        stmt5 = ibm_db.exec_immediate(conn,query)
        row = ibm_db.fetch_tuple(stmt5)
        if(row[0] ==1 ):
            return redirect("/")
        return render_template("/index")

@app.route("/index",methods=('GET','POST'))
def loginpage1():
  return render_template("index.html")




@app.route("/donordetails" , methods=['GET', 'POST'])
def shop():
  sql = "SELECT * FROM USERTBL"
  username = []
  password = []
  stmt = ibm_db.exec_immediate(conn, sql)
  dictionary = ibm_db.fetch_assoc(stmt)
  while dictionary != False:
    username.append(f'{dictionary["USERNAME"]}')
    password.append(f'{dictionary["PASSWORD"]}')
    dictionary = ibm_db.fetch_assoc(stmt)
  return render_template('donordetails.html', len = len(username), username = username, password = password)


if __name__ == "__main__":
    app.run(debug=True)