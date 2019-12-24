FROM python:3.8-alpine
WORKDIR /
COPY ./requirements.txt . 
RUN pip3 install -r requirements.txt
COPY /src/app.py /src/app.py

#CMD bash ./run_db.sh

ENTRYPOINT ["python3", "src/app.py"] 
