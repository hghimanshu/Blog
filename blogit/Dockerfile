FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get --assume-yes --no-install-recommends install \
        build-essential \
        curl \
        git \
        vim

ADD ./ src/
WORKDIR /src

RUN pip install pip==22.1.2
RUN pip install -r requirements.txt
