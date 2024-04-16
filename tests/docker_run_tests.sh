#!/bin/bash
set -e -o pipefail

cd /repo
pip install .

cd ~
python3 /repo/tests/tests_main.py

cat /root/.vault/.database.json
cat /root/.vault/.privatekey

vault set key-test3
vault show key-test3