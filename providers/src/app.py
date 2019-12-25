import random
from flask import Flask, request, Response, jsonify
import requests
import mysql.connector
import csv
import xlrd
from datetime import datetime


app = Flask(__name__)
updated_rates_file = ""


# Send query to the db database in the mysql container.
def send_to_db(sql_query):
    try:
        return send_to_db_host("providers_db", sql_query)
    except:
        return send_to_db_host("providers_db_test", sql_query)


def send_to_db_host(host_name, sql_query):
    db = mysql.connector.connect(
        host=host_name,
        port=3306,
        user="root",
        passwd="12345678",
        # auth_plugin='mysql_native_password',
        database='billdb'
    )
    cursor = db.cursor(buffered=True)
    cursor.execute(sql_query)

    try:
        query_result = cursor.fetchall()
    except mysql.connector.errors.InterfaceError:
        query_result = None

    cursor.close()
    db.close()

    return query_result


@app.route('/health', methods=['GET'])
def health():
    try:
        send_to_db("SELECT 1;")
    except Exception as e:
        return jsonify({'message': "I'M NOT OK", 'status': 500})
    else:
        return jsonify({'message': "OK", 'status': 200})
    cursor.close()
    return


@app.route('/provider', methods=['POST'])
def provider():
    """Insert a provider to the Provider table in the billdb database."""


    def id_in_db(id):
        """Return true if the id number is in the table."""
        query = f'SELECT EXISTS (SELECT id FROM Provider WHERE id={id});'

        query_result = send_to_db(query)[0]

        return query_result


    name = request.form['name']
    id = int(random.random() * 999)

    send_to_db('USE billdb;')

    # If the id number is in the table already, generate another and try again.
    while not id_in_db(id):
        id = int(random.random() * 999)

    send_to_db(f'INSERT INTO Provider VALUES ("{id}", "{name}")')

    return jsonify(id=id), 200


@app.route('/rates', methods=['POST', 'GET'])
def rates():
    global updated_rates_file

    if request.method == 'GET':
        path = "in/" + updated_rates_file

    elif request.method == 'POST':
        updated_rates_file = str(request.form.get("file"))
        path = "in/" + updated_rates_file
        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)

        # create query for full table
        query = "delete from Rates; "
        for i in range(1, sheet.nrows):
            query += "INSERT INTO Rates VALUES (" + str(sheet.row_values(i))[1:-1] + "); "
        # execute query in db
        try:
            send_to_db(query)
        except Exception as e:
            app.logger.info("ERROR: POST rates")
    return ''


@app.route('/truck', methods=['PUT'])
def truck_put():
    truck_id = request.form['truck_id']
    provider_id = request.form['provider_id']

    # Check if truck_id exists in the Provider table of billdb database.
    query = f'SELECT EXISTS (SELECT {truck_id} FROM Trucks WHERE id={truck_id});'
    query_result = send_to_db(query)

    if query_result[0]:
        query = 'UPDATE Trucks SET provider_id={provider_id} WHERE id={truck_id}'
        send_to_db(query)

        return '', 200
    else:
        return '', 404


@app.route('/truck', methods=['POST'])
def truck_post():
    """Receives a truck id(licence plate number) and a provider from the user and insert
    the data into the truck table in the db database.
    """

    # Get form data.
    truckid = request.form['id']
    providerid = request.form['provider']

    # Setup query and data.
    send_to_db('USE billdb;')
    query = f"INSERT INTO Trucks (id, provider_id) VALUES ({truckid}, {providerid});"

    # Insert the truck data in to the trucks table.
    send_to_db(query)

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
    firstName = request.args.get('first_name')
    return '', 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
