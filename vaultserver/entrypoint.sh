#!/bin/bash

cd $VAULT_INSTALL_DIR
pip install .

cd $VAULT_INSTALL_DIR/vaultserver


if [ -z "$VAULT_SERVER_SCALING" ]; then
    export VAULT_SERVER_SCALING=4
fi

if [ "$VAULT_SERVER_MODE" = "debug" ]; then
    echo "VAULT: starting server in debug mode"
    python3 flask_server.py
    #flask --app flask_server run
else
    echo "VAULT: starting server with scaling $VAULT_SERVER_SCALING"
	gunicorn -w $VAULT_SERVER_SCALING -b 0.0.0.0:5000 flask_server:app
    #gunicorn --worker-class sync --workers 4 --bind 0.0.0.0:8000 "myapp:create_app()" --pythonpath `which pypy3`
fi

