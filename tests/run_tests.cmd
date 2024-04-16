

set REPODIR=%~dp0../
set TEST_ENV_NAME=secretsvault-tests

docker build -t %TEST_ENV_NAME% -f %~dp0secretsvault-test-env.dockerfile %~dp0

docker run ^
	--rm ^
	-it ^
	-v %REPODIR%:/repo ^
	-e "TERM=xterm-256color" ^
	%TEST_ENV_NAME% ^
	/bin/bash /repo/tests/docker_run_tests.sh
