FROM python:3.8

COPY . .

RUN apt-get update && apt-get install -y iputils-ping

ENTRYPOINT ["python3", "./find_MTU.py"]