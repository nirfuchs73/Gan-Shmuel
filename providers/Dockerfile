FROM python:3.8-alpine
WORKDIR /src
COPY ./src/app.py .
RUN pip install Flask
RUN pip install requests
RUN pip install mysql-connector-python

ENTRYPOINT ["python3", "app.py"] 
