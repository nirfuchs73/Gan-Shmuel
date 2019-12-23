from flask import Flask, request, Response
import requests
import mysql.connector
import csv
import xlrd

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

@app.route('/health', methods=['GET'])
def health():
    try:
        cursor.execute("SELECT 1;")
    except Exception as e:
        return Response(status=500)
    else:
        return Response(status=200)
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
def truck():
    """Receives a truck id(licence plate number) and a provider from the user and insert
    the data into the truck table in the db database.
    """
    # Get form data.
    truckid = request.post['id']
    providerid = request.form['provider']

    

    # Insert the truck data in to the trucks table.
    cursor.execute(f"INSERT INTO trucks (truckid, providerid) VALUES ('{truckid}', '{providerid}');")

    return

@app.route('/bill', methods=['GET'])
def bill():
    return "empy"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

cursor.close()
db.close()
