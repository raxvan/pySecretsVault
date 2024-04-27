

set REPODIR=%~dp0../
set TEST_ENV_NAME=vaultserver-test-environment

docker build -t %TEST_ENV_NAME% -f %~dp0../vaultserver/server-env.dockerfile %~dp0

mkdir TestVolume

docker run ^
	-it ^
	--rm ^
	--network=host ^
	-p 5000:5000 ^
	-v %~dp0TestVolume:/vault ^
	-v %REPODIR%:/repo ^
	-e "TERM=xterm-256color" ^
	-e "SERVER_MODE=debug" ^
	%TEST_ENV_NAME% ^
	/bin/bash /repo/vaultserver/entrypoint.sh
