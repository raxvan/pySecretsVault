#!/bin/bash
set -e -o pipefail

cd /repo
pip install .

cd /
mkdir vault1_env
cd /vault1_env
python3 /repo/tests/tests_main.py

#cat /root/.vault/.database.json
#cat /root/.vault/.privatekey

mkdir vault1_envtest
cd vault1_envtest
vault list
vault info

cd /
mkdir vault2_env
cd /vault2_env
vault info
#vault create key-user
#vault show key-user

