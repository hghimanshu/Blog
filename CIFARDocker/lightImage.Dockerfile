FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install -y \
        python3-pip \ 
        python3-dev \
        libsm6 \
        libxext6 \
        libxrender-dev \
        wget \
        unzip \
        ffmpeg \
        git

ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /home/CIFARDocker/