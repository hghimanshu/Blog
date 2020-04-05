FROM ubuntu:18.04
MAINTAINER himanshu garg
RUN apt-get update -y && apt-get install -y python3-pip python3-dev libsm6 libxext6 libxrender-dev

# addons
RUN \
    apt-get install -y \
    wget \
    unzip \
    ffmpeg \
    git

COPY . requirements.txt
RUN pip3 install -r requirements.txt