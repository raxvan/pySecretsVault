#!/bin/bash
set -e -o pipefail

cd /repo
pip install .

cd /repo/tests/VaultTestVolume
rm -rf ./data ||:
rm -rf ./config ||:
rm test_file ||:


echo "starting server:"

export VAULT_SERVER_MODE=local
/bin/sh /repo/vaultserver/entrypoint.sh > /repo/tests/VaultTestVolume/output.log 2>&1 &
#/bin/sh /repo/vaultserver/entrypoint.sh

sleep $VAULT_STARTUP_TIME
sleep 5

cd /repo/tests

python3 /repo/tests/main_tests.py

export VAULT_URL=http://127.0.0.1:5000
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
