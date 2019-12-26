from flask import Flask, request
import subprocess
import os
import smtplib
# from email.mime.text import MIMEText as text
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

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
    pusher = data['pusher']
    pusher_email = pusher['email']

    success = True

    success = run_checkout(branch)
    if success:
        success = run_build()
    # if success:
    #     success = run_tests()

    if success and branch == 'master':
        success = check_status()
        if success:
            run_deploy()

    send_notification(success, pusher_email)

    return 'JSON posted'


@app.route("/rollback")
def rollback_post():
    print('-----------------------------------------------')
    print('Running Rollback')
    print('-----------------------------------------------')
    success = True
    head = run_process('git', 'rev-parse --short HEAD')
    master = run_process('git', 'rev-parse --short master')
    # master_1 = run_process('git', 'rev-parse --short master~1')
    print('HEAD=', head)
    print('master=', master)

    branch = 'master'
    if str(head) == str(master):
        branch = 'master~1'

    # success = run_checkout('master')
    if success:
        try:
            # run_process('git', 'checkout master~1')
            run_process('git', 'checkout ' + branch)
        except Exception as err:
            print(err)
            # success = False
    if success:
        run_deploy()

    send_notification(success, 'nirfuchs73@gmail.com')

    return 'Rolling back one version...'


def run_checkout(branch):
    print('-----------------------------------------------')
    print('Running Checkout')
    print('-----------------------------------------------')
    result = True
    arguments = 'checkout ' + branch
    command = 'git'
    try:
        run_process(command, arguments)
        arguments = 'pull'
        run_process(command, arguments)
        # if not run_process(command, arguments):
        #     result = False
        # arguments = 'pull'
        # if not run_process(command, arguments):
        #     result = False
    except:
        result = False
    return result


def run_build():
    print('-----------------------------------------------')
    print('Running Build and Test')
    print('-----------------------------------------------')
    result = True

    docker_compose_we = os.path.join('../../weight', 'docker-compose-test.yml')
    if not os.path.exists(docker_compose_we):
        docker_compose_we = os.path.join('weight', 'docker-compose-test.yml')
    docker_compose_pr = os.path.join(
        '../../providers', 'docker-compose-test.yml')
    if not os.path.exists(docker_compose_pr):
        docker_compose_pr = os.path.join(
            'providers', 'docker-compose-test.yml')

    if os.path.exists(docker_compose_we) and os.path.exists(docker_compose_pr):
        command = 'docker-compose'
        arguments_we = '--file ' + docker_compose_we + ' up --build -d'
        arguments_pr = '--file ' + docker_compose_pr + ' up --build -d'
        try:
            run_process(command, arguments_we)
            run_process(command, arguments_pr)
            # if not run_process(command, arguments_we):
            #     result = False
            # if not run_process(command, arguments_pr):
            #     result = False
        except:
            result = False

        run_process('docker', 'logs weight_tests')
        run_process('docker', 'logs providers_tests')

        arguments_we = '-f ' + docker_compose_we + ' down'
        arguments_pr = '-f ' + docker_compose_pr + ' down'
        try:
            run_process(command, arguments_we)
            run_process(command, arguments_pr)
            # if not run_process(command, arguments_we):
            #     result = False
            # if not run_process(command, arguments_pr):
            #     result = False
        except Exception as err:
            # result = False
            print(err)
    else:
        print('docker-compose file does not exist')
        result = False
    return result


def send_notification(success, pusher_email):
    print('-----------------------------------------------')
    print('Running Notification')
    print('-----------------------------------------------')
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

    # msg = text(body)
    msg = MIMEMultipart(body)
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = ", ".join(to)

    weight_tests = os.path.join('tests', 'weight-tests.txt')
    providers_tests = os.path.join('tests', 'providers-tests.txt')

    files = [weight_tests, providers_tests]
    # get all the attachments
    try:
        for file in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % file)
            msg.attach(part)
    except Exception as err:
        print(err)
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
    print('-----------------------------------------------')
    print('Running Deploy')
    print('-----------------------------------------------')
    result = True
    command = 'docker'

    docker_compose_we = os.path.join('../../weight', 'docker-compose.yml')
    if not os.path.exists(docker_compose_we):
        docker_compose_we = os.path.join('weight', 'docker-compose.yml')
    docker_compose_pr = os.path.join('../../providers', 'docker-compose.yml')
    if not os.path.exists(docker_compose_pr):
        docker_compose_pr = os.path.join('providers', 'docker-compose.yml')

    if os.path.exists(docker_compose_we) and os.path.exists(docker_compose_pr):
        command = 'docker-compose'
        arguments_we = '--file ' + docker_compose_we + ' down'
        arguments_pr = '--file ' + docker_compose_pr + ' down'
        try:
            run_process(command, arguments_we)
            run_process(command, arguments_pr)
            # if not run_process(command, arguments_we):
            #     result = False
            # if not run_process(command, arguments_pr):
            #     result = False
        except:
            result = False

        arguments_we = '--file ' + docker_compose_we + ' up --build -d'
        arguments_pr = '--file ' + docker_compose_pr + ' up --build -d'
        try:
            run_process(command, arguments_we)
            run_process(command, arguments_pr)
            # if not run_process(command, arguments_we):
            #     result = False
            # if not run_process(command, arguments_pr):
            #     result = False
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
    print('-----------------------------------------------')
    print('Running: ' + command + ' ' + arguments)
    print('-----------------------------------------------')
    # file = open(globals.log_file, 'a')
    result = subprocess.call(args)
    if result == 0:
        print('-----------------------------------------------')
        print(command + ' ' + arguments + ' SUCCEEDED')
        print('-----------------------------------------------')

        return True
    else:
        print('-----------------------------------------------')
        print(command + ' ' + arguments + ' FAILED')
        print('-----------------------------------------------')
        return False


def check_status():
    weight_tests = os.path.join('tests', 'weight-tests.txt')
    providers_tests = os.path.join('tests', 'providers-tests.txt')
    weight_status = subprocess.check_output(['tail', '-1', weight_tests])
    providers_status = subprocess.check_output(['tail', '-1', providers_tests])

    w_status = b'OK' in weight_status
    p_status = b'OK' in providers_status

    if w_status and p_status:
        return True
    else:
        return False


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True, port=8081)
