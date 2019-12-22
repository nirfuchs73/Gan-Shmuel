from flask import Flask, request
import mysql.connector
import requests


app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
