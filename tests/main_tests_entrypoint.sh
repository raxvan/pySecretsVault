#!/bin/bash
set -e -o pipefail

cd /repo
pip install .

python3 /repo/tests/main_tests.py

#vault list
#vault info


