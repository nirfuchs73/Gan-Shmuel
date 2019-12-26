FROM python:3.8-alpine

WORKDIR /

COPY ./requirements.txt . 
COPY /src/app.py /src/app.py
COPY /src/index.html /src

RUN pip3 install -r requirements.txt
#CMD bash ./run_db.sh

ENTRYPOINT ["python3", "src/app.py"] 
