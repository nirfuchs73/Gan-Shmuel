FROM python
WORKDIR /app
COPY ./requirments.txt ./
RUN pip install -r requirments.txt
COPY . . 
RUN apt-get upgrade
RUN apt-get install git
ENTRYPOINT ["python3"]
CMD ["ci-server.py"]
