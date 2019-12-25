FROM python:3.6.9-alpine3.10

COPY requirements.txt /app/

WORKDIR /app

RUN pip3 install -r requirements.txt 

COPY test*.py /app/

ENTRYPOINT ["python3", "tests.py"]
