#!/bin/bash
set -e -o pipefail

cd /repo
pip install .

echo "starting server:"
python3 /repo/vaultserver/make_config.py /vault/config

/bin/bash /repo/vaultserver/entrypoint.sh&

sleep 5

cd /repo/tests
python3 /repo/tests/main_tests.py

vault info
vault list
vault get test-key
vault set test-key2 test-value2
vault list





