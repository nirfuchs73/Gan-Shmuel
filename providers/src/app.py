from flask import Flask, request
import mysql.connector
import requests


app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="12345678",
    auth_plugin='mysql_native_password'
)


@app.route('/health', methods=['GET'])
def health():
    return "empty"


@app.route('/provider', methods=['POST'])
def provider():
    return "empty"


@app.route('/rates', methods=['POST', 'GET'])
def rates():
    return "empty"


@app.route('/truck', methods=['POST'])
def truck():
    if request.method == 'POST':
        return "empty"


@app.route('/bill', methods=['GET'])
def bill():
    return "empy"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
