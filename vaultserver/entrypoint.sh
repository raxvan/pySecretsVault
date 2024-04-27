#!/bin/bash

cd /repo
pip install .

cd /repo/vaultserver


if [ "$SERVER_MODE" = "debug" ]; then
    echo "starting server in debug mode"
    python3 flask_server.py
    #flask --app flask_server run
else
    SCALING=4
	gunicorn -w $SCALING -b 0.0.0.0:5000 flask_server:app
    gunicorn --worker-class sync --workers 4 --bind 0.0.0.0:8000 "myapp:create_app()" --pythonpath `which pypy3`

fi

