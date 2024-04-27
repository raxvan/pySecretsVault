FROM python:3.10

RUN apt-get update && apt-get install -y \
	cmake \
	git

RUN pip3 install --upgrade pip && pip3 install \
	pudb \
	requests

