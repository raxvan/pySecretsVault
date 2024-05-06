#!/bin/sh

if [ -z "$VAULT_INSTALL_DIR" ]; then
    echo "VAULT: repository path is required to be set to VAULT_INSTALL_DIR"
    exit -1
fi

cd $VAULT_INSTALL_DIR
pip3 install .

cd $VAULT_INSTALL_DIR/vaultserver

if [ -z "$VAULT_SERVER_MODE" ]; then
    export VAULT_SERVER_MODE=live
fi

if [ -z "$VAULT_SERVER_SCALING" ]; then
    export VAULT_SERVER_SCALING=4
fi

if [ -z "$VAULT_HOST" ]; then
    export VAULT_HOST=0.0.0.0
fi

if [ -z "$VAULT_PORT" ]; then
    export VAULT_PORT=5000
fi

if [ "$VAULT_SERVER_MODE" = "live" ]; then
    python3 ./make_config.py $VAULT_CONFIG_DIR
fi

if [ "$VAULT_SERVER_MODE" = "debug" ]; then
    echo "VAULT: starting server in debug mode"
    python3 flask_server.py
    #flask --app flask_server run
else
    echo "VAULT: starting server with scaling $VAULT_SERVER_SCALING"
    gunicorn -w $VAULT_SERVER_SCALING -b $VAULT_HOST:$VAULT_PORT flask_server:app
    #gunicorn --worker-class sync --workers 4 --bind 0.0.0.0:8000 "myapp:create_app()" --pythonpath `which pypy3`
fi

