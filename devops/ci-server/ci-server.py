from flask import Flask,request

app = Flask(__name__)

@app.route("/")
def root():
    return 'root'

@app.route("/", methods=['POST'])
def post_git():
    print (request.is_json)
    data = request.get_json(force=True)
    # print (data)
    ref = data['ref']
    pusher = data['pusher']
    name = pusher['name']
    email = pusher['email']
    print(ref)
    print(pusher)
    print(name)
    print(email)
    
    return 'JSON posted'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8081)