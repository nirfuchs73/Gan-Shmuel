from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return 'root'

@app.route("/", methods=['POST'])
def post_git():
    print (request.is_json)
    content = request.get_json()
    print (content)
    return 'JSON posted'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8081)