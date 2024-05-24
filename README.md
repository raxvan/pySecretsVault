
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

- VAULT_VERSION=0.0.0
- VAULT_HOST=0.0.0.0
- VAULT_PORT=5000
- VAULT_MAX_REQUEST_SIZE=1048576
- VAULT_CONFIG_DIR/vault/config
- VAULT_DATA_DIR=/vault/data
- VAULT_SERVER_MODE=none/debug/install/revive
- VAULT_PUBLISH_KEY=FALSE

- VAULT_STARTUP_TIME=2
- VAULT_SERVER_SCALING=4
- VAULT_INSTALL_DIR
- VAULT_URL=http://127.0.0.1:5000