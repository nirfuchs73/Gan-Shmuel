from flask import Flask, request, Response, jsonify
import requests
import mysql.connector
import csv
import xlrd

app = Flask(__name__)

# Connect to the db database in the mysql container.
db = mysql.connector.connect(
    host="providers_db",
    port = 3306,
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
        return jsonify({'message':"I'M NOT OK", 'status':500})
    else:
        return jsonify({'message':"OK", 'status':200})
    return

@app.route('/provider', methods=['POST'])
def provider():
    return "empty"

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
            #print(str(sheet.row_values(i))[1:-1])
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

cursor.close()
db.close()
