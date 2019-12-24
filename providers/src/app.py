import random
from flask import Flask, request, Response, jsonify
import requests
import mysql.connector
import csv
import xlrd
from datetime import datetime


app = Flask(__name__)

# Connect to the db database in the mysql container.
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="12345678",
    # auth_plugin='mysql_native_password',
    # database='billdb'
)
cursor = db.cursor()


@app.route('/health', methods=['GET'])
def health():
    try:
        cursor.execute("SELECT 1;")
    except Exception as e:
        return jsonify({'message': "I'M NOT OK", 'status': 500})
    else:
        return jsonify({'message': "OK", 'status': 200})
    return


@app.route('/provider', methods=['POST'])
def provider():
    """Insert a provider to the Provider table in the billdb database."""


    def id_in_db(id):
        """Return true if the id number is in the table."""
        query = 'SELECT EXISTS (SELECT id FROM Provider WHERE id=%s);'
        cursor.execute(query, [id])

        return cursor.fetchone()[0]


    name = request.form['name']
    id = int(random.random() * 999)

    cursor.execute('USE billdb;')

    # If the id number is in the table already, generate another and try again.
    while id_in_db(id):
        id = int(random.random() * 999)

    cursor.execute('INSERT INTO Provider VALUES (%s, %s)', [id, name])
    db.commit()

    return jsonify(id=id), 200


@app.route('/rates', methods=['POST', 'GET'])
def rates():
    if request.method == 'GET':
        return "empty"

    elif request.method == 'POST':
        rf = request.form
        path = "in/" + str(rf.get("file"))
        # TODO save file in mysql volume?
        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)
        cursor.execute("delete from Rates;")
        for i in range(1, sheet.nrows):
            # print(str(sheet.row_values(i))[1:-1])
            cursor.execute("INSERT INTO Rates VALUES (" + str(sheet.row_values(i))[1:-1] + ");")

    return "empy"


@app.route('/truck', methods=['POST'])
def truck_post():
    """Receives a truck id(licence plate number) and a provider from the user and insert
    the data into the truck table in the db database.
    """

    # Get form data.
    truckid = request.form['id']
    providerid = request.form['provider']

    # Setup query and data.
    cursor.execute('USE billdb;')
    query = "INSERT INTO Trucks (id, provider_id) VALUES (%s, %s);"
    data = (truckid, providerid)

    # Insert the truck data in to the trucks table.
    cursor.execute(query, data)
    db.commit()

    return '', 200


@app.route('/truck/<truckid>/', methods=['GET'])
def truck_get(truckid):
    """Returns a json file containing all the trucks between the
     1st of the month to the current date.
     Returns 404 if the database does not contain trucks between the specified dates"""

    _from = datetime.now().strftime('%Y%m01000000')
    _to = datetime.now().strftime('%Y%m%d%H%M%S')

    item = requests.get(f'localhost:8090/unit/{truckid}', {'from': _from, 'to': _to})

    return item, 200


@app.route('/bill', methods=['GET'])
@app.route('/')
def bill():
    return '', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

cursor.close()
db.close()
