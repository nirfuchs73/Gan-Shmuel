from flask import Flask, request
import subprocess
import os
import smtplib

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
    pusher_name = pusher['name']
    pusher_email = pusher['email']
    print(ref)
    print(repo_name)
    print(pusher)
    print(pusher_name)
    print(pusher_email)

    success = True

    success = run_checkout(branch)
    if success:
        success = run_build()
    if success:
        success = run_tests()

    send_notification(success, pusher_email)

    if success and branch == 'master':
        run_deploy()

    return 'JSON posted'


def run_checkout(branch):
    print('run_checkout')
    arguments = 'checkout '+ branch
    command = 'git'
    try:
        if not run_process(command, arguments):
            result = False
    except:
        result = False
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


def send_notification(success, pusher_email):
    print('Run Notification')
    result = True
    gmail_user = 'ci.server73@gmail.com'
    gmail_password = '1q2w#E$R'
    sent_from = gmail_user
    to = [pusher_email, 'nirfuchs73@gmail.com']

    message = 'Build completed successfully'
    if not success:
        message = 'Build failed'
    subject = message
    body = message
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    print(email_text)

    try:
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        # server.sendmail(sent_from, to, email_text)
        server.sendmail(sent_from, to, 'test email')

        server.close()
    except Exception as err:
        print(err)
        print('Something went wrong...')
        result = False

    return result


def run_deploy():
    result = True
    print('run_deploy')
    docker_compose_file = os.path.join('../../', 'docker-compose.yml')
    if os.path.exists(docker_compose_file):
        command = 'docker-compose'
        arguments = '--file ' + docker_compose_file + ' down -d '
        try:
            if not run_process(command, arguments):
                result = False
        except:
            result = False

        argumentsForUp = '--file ' + docker_compose_file + ' up -d '
        try:
            if not run_process(command, argumentsForUp):
                result = False
        except:
            result = False

    else:
        print(docker_compose_file + ' does not exist')
        result = False
        return result

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
    send_notification(True, 'nirfuchs@hotmail.com')
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8081)
