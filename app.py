import os
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

# SQL Connection ======================================================
app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = "ai"
# app.config['MYSQL_PASSWORD'] = "kongu"
app.config['MYSQL_USER'] = os.getenv('MYSQL_ADMIN_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_ADMIN_PASSWORD')
app.config['MYSQL_DB'] = 'test'
# ======================================================================
mysql = MySQL(app)

@app.route('/fetchall', methods = ['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM user"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/insert', methods = ['GET', 'POST'])
def insert():
    if request.method == 'GET':
        return jsonify({"Status":False, 'message': 'Method not allowed'}), 405
    
    # Data from front-end ===========================
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    # ===============================================

    try:
        cur = mysql.connection.cursor()
        s = "INSERT INTO user (user_id, password) VALUES (%s, %s)"
        cur.execute(s, (user_id, password))
        mysql.connection.commit() # Yesterdays mistake
        cur.close()
        return jsonify({"Status": True, "message": "Data inserted successfully"})
    except mysql.connection.IntegrityError as e:
        return jsonify({"Status": False, "message": "Duplicate entry for primary key", "Error":str(e)})