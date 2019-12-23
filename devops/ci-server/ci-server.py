from flask import Flask, request
import subprocess
import os

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
    branch = ref.rsplit('/', 1)[1]
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

    success = run_checkout(branch)
    if success:
        success = run_build()
    if success:
        success = run_tests()

    send_notification(success)

    if success and ref == 'refs/heads/master':
        run_deploy()

    return 'JSON posted'


def run_checkout(branch):
    full_args = 'checkout '+ branch
    result = run_process('git', full_args)
    print('run_checkout')
    return result

def run_build():
    print('Run Build')
    result = True
    docker_compose_file = os.path.join('../../', 'docker-compose-test.yml')
    if os.path.exists(docker_compose_file):
        command = 'docker-compose'
        arguments = '--file ' + docker_compose_file + ' up --build'
        try:
            if not run_process(command, arguments):
                result = False
        except:
            result = False
    else:
        print(docker_compose_file + ' does not exist')
        result = False
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


# run process
def run_process(command, arguments):
    args = [command]
    arguments_list = arguments.split(' ')
    args.extend(arguments_list)
    print('Running: ' + command + ' ' + arguments)
    # file = open(globals.log_file, 'a')
    result = subprocess.call(args)
    if result == 0:
        print(command + ' ' + arguments + ' succeeded')
        return True
    else:
        print(command + ' ' + arguments + ' failed')
        return False


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8081)
