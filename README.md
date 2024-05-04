
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

