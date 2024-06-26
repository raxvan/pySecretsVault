
# pySecretsVault

For secrets management. This package provides functionality for key/value pairs storage where the value is encoded.

# Quick start

```
import secretsvault

config = {
	"url" : "..."
}
v = secretsvault.CreateVault(config)

v["key"] = "value"

print(v["key"])

```

# Environment variables used

- VAULT_NAME=none
- VAULT_HOST=0.0.0.0
- VAULT_PORT=5000
- VAULT_MAX_REQUEST_SIZE=1048576
- VAULT_CONFIG_DIR/vault/config
- VAULT_DATA_DIR=/vault/data
- VAULT_LOGS_DIR=/vault/logs
- VAULT_SERVER_MODE=none/debug/live
- VAULT_PUBLIC_ACCESS=none/enable/subnet
- VAULT_STARTUP_TIME=2 #in seconds

- VAULT_INSTALL_DIR
- VAULT_URL=http://127.0.0.1:5000

# Server requirements:

- gunicorn
- flask
- netifaces
- shared-memory-dict

Starting the server locally (first install with pip):
```
vault config-create-unsafe
/bin/sh pySecretsVault/vaultserver/entrypoint.sh > vault/server.log 2>&1 &
```
