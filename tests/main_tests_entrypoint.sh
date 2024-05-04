#!/bin/bash
set -e -o pipefail

cd /repo
pip install .

cd /repo/tests/VaultTestVolume
rm -rf ./data ||:
rm -rf ./config ||:
rm test_file ||:


echo "starting server:"

/bin/bash /repo/vaultserver/entrypoint.sh&

sleep 2

cd /repo/tests

python3 /repo/tests/main_tests.py

vault info
vault list
vault get test-key
vault set test-key2 test-value2
vault list


vault edit ./VaultTestVolume/test_file
vault cat ./VaultTestVolume/test_file
vault list