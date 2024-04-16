#!/bin/bash

cd /repo
pip install .

cd ~
python3 /repo/tests/tests_main.py