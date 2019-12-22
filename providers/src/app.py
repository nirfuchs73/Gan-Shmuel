from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return "empty"

@app.route('/provider', methods=['POST'])
def provider():
    return "empty"

@app.route('/rates', methods=['POST', 'GET'])
def rates():
    if request.method == 'POST':
        return "empty"
        
    elif request.method == 'GET':
        return "empty"
    return "empy"

@app.route('/truck', methods=['POST', 'GET', 'PUT'])
def truck():
    if request.method == 'POST':
        return "empty"
        
    elif request.method == 'GET':
        return "empty"

    elif request.method == 'PUT':
        return "empty"
    return "empy"

@app.route('/bill', methods=['GET'])
def bill():
    return "empy"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


