from flask import Flask, request
import subprocess
import os
import smtplib
from email.mime.text import MIMEText as text

app = Flask(__name__)


@app.route("/")
def root():
    return 'CI Server is running !!!'


@app.route("/", methods=['POST'])
def post_git():
    print(request.is_json)
    data = request.get_json(force=True)
    ref = data['ref']
    branch = ref.rsplit('/', 1)[1]
    # repository = data['repository']
    # repo_name = repository['name']
    pusher = data['pusher']
    # pusher_name = pusher['name']
    pusher_email = pusher['email']
    # print(ref)
    # print(repo_name)
    # print(pusher)
    # print(pusher_name)
    # print(pusher_email)

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
    print('Run Checkout')
    result = True
    arguments = 'checkout ' + branch
    command = 'git'
    try:
        if not run_process(command, arguments):
            result = False
        arguments = 'pull'
        if not run_process(command, arguments):
            result = False
    except:
        result = False
    return result


def run_build():
    print('Run Build')
    result = True
    docker_compose_we = os.path.join('../../weight', 'docker-compose-test.yml')
    docker_compose_pr = os.path.join('../../providers', 'docker-compose-test.yml')

    if os.path.exists(docker_compose_we) and os.path.exists(docker_compose_pr):
        command = 'docker-compose'
        arguments_we = '--file ' + docker_compose_we + ' up --build -d'
        arguments_pr = '--file ' + docker_compose_pr + ' up --build -d'
        try:
            if not run_process(command, arguments_we):
                result = False
            if not run_process(command, arguments_pr):
                result = False
        except:
            result = False
    else:
        print('docker-compose file does not exist')
        result = False
    return result


def run_tests():
    print('Run Tests')
    result = True
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

    msg = text(body)
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = ", ".join(to)
    print(sent_from)
    print(to)
    print(msg.as_string())

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, msg.as_string())
        server.close()
    except Exception as err:
        print(err)
        print('Something went wrong...')
        result = False

    return result


def run_deploy():
    result = True
    print('Run Deploy')
    docker_compose_we = os.path.join('../../weight', 'docker-compose.yml')
    docker_compose_pr = os.path.join('../../providers', 'docker-compose.yml')
    if os.path.exists(docker_compose_we) and os.path.exists(docker_compose_pr):
        command = 'docker-compose'
        arguments_we = '--file ' + docker_compose_we + ' down -d'
        arguments_pr = '--file ' + docker_compose_pr + ' down -d'
        try:
            if not run_process(command, arguments_we):
                result = False
            if not run_process(command, arguments_pr):
                result = False
        except:
            result = False

        arguments_we = '--file ' + docker_compose_we + ' up --build -d'
        arguments_pr = '--file ' + docker_compose_pr + ' up --build -d'
        try:
            if not run_process(command, arguments_we):
                result = False
            if not run_process(command, arguments_pr):
                result = False
        except:
            result = False
    else:
        print('docker-compose file does not exist')
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
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8081)
