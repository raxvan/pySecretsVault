

set REPODIR=%~dp0../
set TEST_ENV_NAME=secretsvault-tests

docker build -t %TEST_ENV_NAME% -f %~dp0test-env.dockerfile %~dp0

docker run ^
	-it ^
	--rm ^
	--network testing ^
	--publish 5000:5000 ^
	-v %REPODIR%:/repo ^
	-v %REPODIR%/tests/VaultTestVolume:/vault ^
	-e "TERM=xterm-256color" ^
	-e "VAULT_SERVER_MODE=debug" ^
	%TEST_ENV_NAME% ^
	/bin/bash /repo/tests/main_tests_entrypoint.sh
