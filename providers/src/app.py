from flask import Flask, request
import requests
import mysql.connector
import csv

app = Flask(__name__)

sql = mysql.connector.connect(user='root', password='12345678',
                            host='localhost',
                            database='db')
cursor = sql.cursor()

@app.route('/health', methods=['GET'])
def health():
    return "empty"

@app.route('/provider', methods=['POST'])
def provider():
    return "empty"

@app.route('/rates', methods=['POST', 'GET'])
def rates():
    if request.method == 'POST':
        path = "/in/" + str(request.form.get("file"))
        # TODO save file in mysql volume?
        with open(path, 'rb') as csvfile:
            
        cursor.execute('insert into test_table ...')
        return "empty"
        
    elif request.method == 'GET':
        return "empty"
    return "empy"

@app.route('/truck', methods=['POST'])
def truck():
    """Receives a truck id(licence plate number) and a provider from the user and insert
    the data into the truck table in the db database.
    """
    # Get form data.
    truckid = request.post['id']
    providerid = request.form['provider']

    # Connect to the db database in the mysql container.
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="12345678",
        auth_plugin='mysql_native_password',
        database='db'
    )
    cursor = db.cursor()

    # Insert the truck data in to the trucks table.
    cursor.execute(f"INSERT INTO trucks (truckid, providerid) VALUES ('{truckid}', '{providerid}');")

    return

@app.route('/bill', methods=['GET'])
def bill():
    return "empy"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

conn.close()
