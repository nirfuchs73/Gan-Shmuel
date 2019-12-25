FROM python:3.6.9-alpine3.10
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY tests.py ./
ENTRYPOINT ["python3", "tests.py"]
