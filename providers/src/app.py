from flask import Flask, request
import requests
import mysql.connector
import csv


app = Flask(__name__)

# Connect to the db database in the mysql container.
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="12345678",
    auth_plugin='mysql_native_password',
    database='db'
)
cursor = db.cursor()


# @app.route('/health', methods=['GET'])
# def health():
#     return "empty"
#
#
# @app.route('/provider', methods=['POST'])
# def provider():
#     return "empty"
#
#
# @app.route('/rates', methods=['POST', 'GET'])
# def rates():
#     if request.method == 'POST':
#         path = "/in/" + str(request.form.get("file"))
#         # TODO save file in mysql volume?
#         with open(path, 'rb') as csvfile:
#
#         cursor.execute('insert into test_table ...')
#         return "empty"
#
#     elif request.method == 'GET':
#         return "empty"
#     return "empy"


@app.route('/truck', methods=['POST'])
def truck_post():
    """Receives a truck id(licence plate number) and a provider from the user and insert
    the data into the truck table in the db database.
    """
    # Get form data.
    truckid = request.form['id']
    providerid = request.form['provider']

    query = "INSERT INTO db.trucks (truckid, providerid) VALUES (%s, %s);"
    data = (truckid, providerid)

    # Insert the truck data in to the trucks table.
    cursor.execute(query, data)

    db.commit()

    return '', 200


@app.route('/truck/<truckid>/', methods=['GET'])
def truck_get(truckid):
    _from = request.args.get('from')
    _to = request.args.get('to')

    return '', 200


@app.route('/bill', methods=['GET'])
@app.route('/')
def bill():
    return '', 200


app.run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
