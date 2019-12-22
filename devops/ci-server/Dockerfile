FROM python
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./
RUN apt-get upgrade
RUN apt-get install git
ENTRYPOINT ["python3"]
CMD ["ci-server.py"]
