
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
- VAULT_SERVER_MODE=none/debug/install/revive
- VAULT_PUBLIC_ACCESS=none/enable/subnet

- VAULT_SERVER_SCALING=4
- VAULT_INSTALL_DIR
- VAULT_URL=http://127.0.0.1:5000

# Server requirements:

gunicorn
flask
