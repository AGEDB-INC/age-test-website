from flask import Flask,redirect,url_for,render_template,redirect,request,session,flash
from flask_session import Session
import psycopg2 as pg2
from psycopg2 import connect
from psycopg2 import DatabaseError, DataError, InternalError, NotSupportedError, OperationalError
app=Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
@app.route("/")
def home():
    #session.clear()
    return render_template("index.html")
def DB(dbname,host,port,username,password):
    try:
        conn=pg2.connect(database=dbname,host=host,port=port,user=username,password=password)
        conn.autocommit = True
        try:
            cur=conn.cursor()
            conn.commit()
            print('database connection')
        except:
            print('database connection exception')
        finally:
            cur.close()
        return conn
    except OperationalError as err:
        return "error"
@app.route("/dbconnect", methods=["POST", "GET"])
def dbconnect():
  # if form is submited
    if request.method == "POST":
        dbtype= request.form.get("dbtype")
        version= request.form.get("dbver")
        host= request.form.get("host")
        dbname= request.form.get("dbname")
        port= request.form.get("port")
        username= request.form.get("uname")
        password= request.form.get("pname")
        edit= request.form.get("edit")
        conn=DB(dbname,host,port,username,password)
        if conn !="error":
            if edit!="0":
                print("i am here")
                if edit in session:
                    session.pop(edit, None)
                    session[dbtype+"_"+version]=[dbtype,version,host,dbname,port,username,password]
                    flash('Database ifornamtion is updated') 
            else:
                session[dbtype+"_"+version]=[dbtype,version,host,dbname,port,username,password]
                print("database is connected")
                flash('Database is connected')
            render_template("index.html")
        else:
            print("database is not connected")
            flash('Cannot connect to database.')
            render_template("index.html")
    return render_template("index.html")

@app.route("/edit/<edititem>", methods=["POST", "GET"])
def editdbifo(edititem):
    return render_template("index.html",edit=edititem)

if __name__=="__main__":

    app.run(debug=True)
    session.clear()
