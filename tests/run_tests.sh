#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


REPODIR=$THIS_DIR/../
TEST_ENV_NAME=secretsvault-tests

docker build -t $TEST_ENV_NAME -f $THIS_DIR/secretsvault-test-env.dockerfile $THIS_DIR

docker run \
	--rm \
	-it \
	-v $REPODIR:/repo \
	-e "TERM=xterm-256color" \
	$TEST_ENV_NAME \
	python3 /repo/tests/run_tests.py
