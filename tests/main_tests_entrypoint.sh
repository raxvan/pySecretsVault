#!/bin/bash
set -e -o pipefail

cd /repo
pip install .

cd /repo/tests
#python3 /repo/tests/main_tests.py

vault info
vault list
vault get test-key
vault set test-key2 test-value2
vault list
vault 




