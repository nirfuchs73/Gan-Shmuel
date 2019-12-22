from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return 'root'

@app.route("/", methods=['POST'])
def post_git():
    return 'POST'  

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8081)