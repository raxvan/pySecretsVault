#!/bin/sh

if [ -z "$VAULT_INSTALL_DIR" ]; then
    echo "VAULT: repository path is required to be set to VAULT_INSTALL_DIR"
    exit -1
fi

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

if [ -z "$VAULT_STARTUP_TIME" ]; then
    export VAULT_STARTUP_TIME=2
fi

python3 $VAULT_INSTALL_DIR/vaultserver/vaultconfig.py &

echo "VAULT: Starting up with mode $VAULT_SERVER_MODE ..."
sleep $VAULT_STARTUP_TIME

if [ "$VAULT_SERVER_MODE" = "debug" ]; then
    #flask --app vaultapp run
    python3 vaultapp.py
else
    echo "VAULT: Scaling $VAULT_SERVER_SCALING"
    gunicorn \
        --workers $VAULT_SERVER_SCALING \
        --bind $VAULT_HOST:$VAULT_PORT \
        --error-logfile %VAULT_DATA_DIR/.vault.error.log \
        vaultapp:app
fi

