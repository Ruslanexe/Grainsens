from flask import Flask
from flask import render_template, request
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
            f"VALUES({branch_id},{mgr_id},'{send_info_date}',{temperature})"
        )
        cnx.commit()
        cur.close()
        return render_template()
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


app.run(debug=True)
