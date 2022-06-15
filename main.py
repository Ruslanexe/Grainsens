import MySQLdb.cursors
import bcrypt
from flask import Flask, session, flash
from flask import render_template, request, url_for, redirect
import mysql.connector

app = Flask(__name__)

cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='20041516',
    database='giraffe',
    auth_plugin='mysql_native_password'
)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/create-branch', methods=['POST', 'GET'])
def create_branch():
    if request.method == 'POST':
        branch_id = request.form['branch_id']
        mgr_id = request.form['mgr_id']
        send_info_date = request.form['send_info_date']
        temperature = request.form["temperature"]
        cur = cnx.cursor()
        cur.execute(
            f"INSERT INTO branch(branch_id,mgr_id,send_info_date,temperature)"
            f"VALUES({branch_id},{mgr_id},{send_info_date},{temperature})")
        cnx.commit()
        cur.close()
        return "POST SUCCESS"
    elif request.method == 'GET':
        return render_template('create_branch.html')
    return "Wrong "


@app.route('/create-device', methods=['POST', 'GET'])
def create_device():
    if request.method == 'POST':
        device_id = request.form['device_id']
        owner_id = request.form['owner_id']
        cur = cnx.cursor()
        cur.execute(f"INSERT INTO device(device_id, owner_id)"
                    f"VALUES({device_id},{owner_id})")
        cnx.commit()
        cur.close()
        return "POST SUCCESS"
    elif request.method == 'GET':
        return render_template('create_device.html')
    return "Fail"

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        sql_statement = f'INSERT INTO user(name,email, password) VALUES("{name}","{email}","{password}")'
        print(sql_statement)
        cur = cnx.cursor()
        cur.execute(sql_statement)
        cnx.commit()
        cur.close()
        return render_template('after_loggin.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']

        sql_statement2 = f'SELECT * FROM user WHERE email="{email}"'
        cur = cnx.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql_statement2)
        user = cur.fetchone()
        try:
            cur.close()
        except Exception:
            print("Exception")

        if len(user)>0:
            if password == user[2]:
                return render_template('after_loggin.html')
            else:
                return str(user[2])
        else:
            return 'Error password or user not match'
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')


app.run(debug=True)
