import os
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

# SQL Connection ======================================================
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_ADMIN_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_ADMIN_PASSWORD')
app.config['MYSQL_DB'] = 'test'
# ======================================================================
mysql = MySQL(app)

@app.route('/fetchall', methods = ['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    # SELECT column1, column2, ...
    # FROM table_name
    sql = "SELECT * FROM user"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/insert', methods = ['GET', 'POST'])
def insert():
    if request.method == 'POST':
        
        # Data from front-end ===========================
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        # ===============================================

        try:

            # INSERT INTO table_name (column1, column2, column3, ...)
            # VALUES (value1, value2, value3, ...)
            cur = mysql.connection.cursor()
            s = "INSERT INTO user (user_id, password) VALUES (%s, %s)"
            cur.execute(s, (user_id, password))
            mysql.connection.commit() # Yesterdays mistake
            cur.close()
            return jsonify({"Status": True, "message": "Data inserted successfully"})
        except mysql.connection.IntegrityError as e:
            return jsonify({"Status": False, "message":str(e)})
        
    else:
        return jsonify({"Status":False, 'message': 'Method not allowed'}), 405

@app.route('/update_password', methods=['POST'])
def update_password():
    if request.method == 'POST':

        # Data from front-end ===========================
        data = request.get_json()
        user_id = data.get('user_id')
        new_password = data.get('new_password')
        # ===============================================

        try:

            # UPDATE table_name
            # SET column1 = value1, column2 = value2, ...
            # WHERE condition
            cur = mysql.connection.cursor()
            sql = "UPDATE user SET password = %s WHERE user_id = %s"
            cur.execute(sql, (new_password, user_id))
            mysql.connection.commit()
            cur.close()

            return jsonify({"Status": True, "message": "Password updated successfully"})
        except Exception as e:
            return jsonify({"Status": False, "message": str(e)})
    else:
        return jsonify({"Status": False, "message": "Method not allowed"}), 405