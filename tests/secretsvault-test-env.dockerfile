FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
	python3-dev \
	python3-pip \
	cmake \
	git


RUN pip3 install --upgrade pip && pip3 install \
	pudb \
	pyoqs-sdk \
	cryptography

