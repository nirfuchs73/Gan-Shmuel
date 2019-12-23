from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def root():
    return 'root'


@app.route("/", methods=['POST'])
def post_git():
    print(request.is_json)
    data = request.get_json(force=True)
    # print (data)
    ref = data['ref']
    repository = data['repository']
    repo_name = repository['name']
    pusher = data['pusher']
    name = pusher['name']
    email = pusher['email']
    print(ref)
    print(repo_name)
    print(pusher)
    print(name)
    print(email)

    success = True

    success = run_checkout(ref)
    if success:
        success = run_build()
    if success:
        success = run_tests()

    send_notification(success)

    if success and ref == 'refs/heads/master':
        run_deploy()

    return 'JSON posted'


def run_checkout(ref):
    result = True
    print('run_checkout')
    return result


def run_build():
    result = True
    print('run_build')
    print('docker-compose up --build')
    return result


def run_tests():
    result = True
    print('run_test')
    return result


def send_notification(success):
    result = True
    print('send_notification')
    return result


def run_deploy():
    result = True
    print('run_deploy')
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8081)
