FROM ubuntu:latest
MAINTAINER  'desunovu@gmail.com'
RUN apt-get update -y
RUN apt-get install -y python-pip python3 build-essential
COPY . /backend
WORKDIR /backend
RUN pip install -r requirements.txt
EXPOSE 5000
