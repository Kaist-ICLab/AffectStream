FROM python:3.9.16-slim

COPY requirements.txt /

RUN apt update
RUN apt install -y git gcc g++ make libssl-dev curl \
    && pip install -r /requirements.txt

ADD src /src
ADD data /data

WORKDIR /src

ENTRYPOINT ["locust"]
