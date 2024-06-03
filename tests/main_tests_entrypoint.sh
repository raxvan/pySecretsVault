#!/bin/bash
set -e -o pipefail

cd /repo

cd /repo/tests/VaultTestVolume
rm -rf ./data ||:
rm -rf ./config ||:
rm test_file ||:

cd /repo/tests/VaultTestVolume

mkdir -p config
mkdir -p data

cd /repo
pip3 install .

echo "Starting server (idle: 5 sec)..."

export VAULT_SERVER_MODE=debug
export VAULT_STARTUP_TIME=2

cd /repo/tests/VaultTestVolume/config

vault config-create keys
vault config-decode keys

#/bin/sh /repo/vaultserver/entrypoint.sh
/bin/sh /repo/vaultserver/entrypoint.sh > /repo/tests/VaultTestVolume/output.log 2>&1 &

sleep 3
export VAULT_URL=http://127.0.0.1:5000

echo -----------------------------------------------------------

cd /repo/tests

python3 /repo/tests/main_tests.py

echo -----------------------------------------------------------

echo "INFO:"
vault info
echo "LIST:"
vault list

echo "SET(kv):"
vault set test-key2 test-value2
echo "SET(k):"
vault set test-key3

echo "GET (missing):"
vault get test-key
echo "GET (found):"
vault get test-key2

echo "LIST(r):"
vault list test-.*
echo "FIND:"
vault find test-.*

vault edit ./VaultTestVolume/test_file
vault cat ./VaultTestVolume/test_file
