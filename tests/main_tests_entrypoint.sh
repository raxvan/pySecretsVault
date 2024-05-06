#!/bin/bash
set -e -o pipefail

cd /repo
pip install .

cd /repo/tests/VaultTestVolume
rm -rf ./data ||:
rm -rf ./config ||:
rm test_file ||:


echo "starting server:"

export VAULT_PUBLISH_KEY=TRUE
export VAULT_SERVER_MODE=local
/bin/sh /repo/vaultserver/entrypoint.sh > /repo/tests/VaultTestVolume/output.log 2>&1 &

sleep $VAULT_STARTUP_TIME
sleep 5

cd /repo/tests

python3 /repo/tests/main_tests.py

echo "INFO:"
vault info
echo "LIST:"
vault list
echo "GET:"
vault get test-key
echo "SET(kv):"
vault set test-key2 test-value2
echo "SET(k):"
vault set test^key3
echo "LIST(r):"
vault list test-.*
echo "FIND:"
vault find test-.*

vault edit ./VaultTestVolume/test_file
vault cat ./VaultTestVolume/test_file
