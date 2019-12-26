import random
from flask import Flask, request, Response, jsonify, send_file
import requests
import mysql.connector
import csv
import xlrd
import os
from datetime import datetime
import json
from collections import OrderedDict


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

# create json for prev_db
def product_json(prev_prod, provider_id, count, transaction):
    rate = send_to_db("select rate from Rates where product_id='" + prev_prod + "' and scope='" + provider_id + "';")
    amount = transaction['bruto']
    if amount=="na":
        amount = 1
    if not rate:
        rate = send_to_db("select rate from Rates where product_id='" + prev_prod + "' and scope='All';")
        if not rate:
            rate = 0
        else:
            rate = rate[0][0]
    else:
        rate = rate[0][0]
    pay = rate * count * amount
    return {'prod': prev_prod, 'count': count, 'amount': amount, 'rate': rate, 'pay': pay}



@app.route('/')
def index():
    return open('/src/index.html').read()


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
    # global updated_rates_file

    if request.method == 'GET':
        path = os.popen('cat src/bin/rates.txt').read().rstrip()
        try:
            return send_file(path, as_attachment=True)
        except FileNotFoundError:
            return "file not found 404"

    elif request.method == 'POST':
        path = "/in/" + str(request.form.get("file"))
        os.system("echo '" + path + "' > " + "src/bin/rates.txt")
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
            return 'Insert error.', 500

    return '', 200


@app.route('/truck', methods=['PUT'])
def truck_put():
    truck_id = request.args['truck_id']
    provider_id = request.args['provider_id']

    # Check if truck_id exists in the Trucks table of billdb database.
    query = f'SELECT EXISTS (SELECT {truck_id} FROM Trucks WHERE id={truck_id});'
    query_result = send_to_db(query)

    if query_result[0]:
        query = f"UPDATE Trucks SET provider_id={provider_id} WHERE id='{truck_id}'"
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
    query = f"INSERT INTO Trucks (id, provider_id) VALUES ('{truckid}', {providerid});"

    # Insert the truck data in to the trucks table.
    send_to_db(query)

    return '', 200


@app.route('/truck/<truckid>/', methods=['GET'])
def truck_get(truckid):
    """Returns a json file containing all the trucks between the
     1st of the month to the current date.
     Returns 404 if the database does not contain trucks between the specified dates"""

    _from = request.args['from']
    _to = request.args['to']

    now = datetime.today()
    first_of_month = datetime(now.year, now.month, 1)
    _from_in_format = datetime.strptime(_from, '%Y%m01000000')
    _to_in_format = datetime.strptime(_to, '%Y%m%d%H%M%S')

    if _from_in_format == first_of_month and _to_in_format <= now:
        item = requests.get(f'http://localhost:8090/item/{truckid}', {'from': _from, 'to': _to})

        return item, 200

    return 'ERROR', 404
  

@app.route('/bill/<provider_id>', methods=['GET'])
def bill(provider_id):
    start = request.args.get('from')
    end = request.args.get('to')

    name = ""
    truck_list = []
    transaction_list = []
    truck_count = 0
    session_count = 0
    total_pay = 0
    prod_list = []

    name = send_to_db("SELECT name FROM Provider WHERE id=" + provider_id + ";")[0][0]

    # get list of transactions between given dates:
    receive = requests.get("http://localhost:8090/weight?from=" + start + "&to=" + end + "&filter=out")
    transaction_list = json.loads(receive.content)
    
    for transaction in transaction_list:
        # get truck id assosiated with transaction
        receive_truck = requests.get('http://localhost:8090/session/' + str(transaction['id']))
        # check if truck belongs to given provider
        truck_id = str(json.loads(receive_truck.content)['truck'])
        app.logger.info("truck-id: " + truck_id)
        if truck_id != "na":
            q = send_to_db("SELECT provider_id FROM Trucks WHERE id='" + truck_id + "' AND provider_id='" + provider_id + "';")
            if q:
                app.logger.info("provider found")
                if truck_id not in truck_list:
                    truck_list.append(truck_id)
                    app.logger.info("truck added")
            else:
                transaction_list.remove(transaction)
                app.logger.info("transaction removed")
        else:
            transaction_list.remove(transaction)
   
    truck_count = len(truck_list)
    session_count = len(transaction_list)
    app.logger.info("truck-count: " + str(truck_count) + " sessions: " + str(session_count))

    # sort transactions by produce
    transaction_list.sort(key=lambda s: s['produce'])
    # initialize vars:
    prev_prod = str(transaction['produce'])
    count = 1
    for transaction in transaction_list[1:]:
        prod = str(transaction['produce'])
        if prod == prev_prod:
            count += 1
            app.logger.info("prod counted: " + prod + " " + str(count))
        else:
            # create product json
            spec_prod_data = product_json(prev_prod, provider_id, count, transaction)
            total_pay += spec_prod_data['pay']
            prod_list.append(spec_prod_data)
            count = 1
        prev_prod = prod

    spec_prod_data = product_json(prev_prod, provider_id, count, transaction)
    total_pay += spec_prod_data['pay']
    prod_list.append(spec_prod_data)

    start = datetime.strptime(start, '%Y%m%d%H%M%S')
    start.strftime("%m/%d/%Y, %H:%M:%S")
    end = datetime.strptime(end, '%Y%m%d%H%M%S')
    end.strftime("%m/%d/%Y, %H:%M:%S")

    bill = OrderedDict({'id': provider_id, 'name': name, 'from': start, 'to': end, 'truckCount': truck_count, 'sessionCount': session_count, 'products': prod_list, 'total': total_pay})
    return jsonify(bill)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
