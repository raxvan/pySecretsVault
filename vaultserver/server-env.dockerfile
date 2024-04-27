FROM python:3.10

RUN apt-get update && apt-get install -y \
	pypy3 \
	cmake \
	git


RUN pip3 install --upgrade pip && pip3 install \
	cryptography \
	flask \
	gunicorn \
	pudb

EXPOSE 5000

CMD ["/bin/bash","/repo/vaultserver/entrypoint.sh"]
