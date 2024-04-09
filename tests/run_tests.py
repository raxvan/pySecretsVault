
import os
import sys
import json


_this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(_this_dir,".."))


import secretsvault

print(json.dumps(secretsvault.details(), indent = 4))


enc = secretsvault.CreateFernetEncoder("test-salt")

vault = secretsvault.Vault(enc)

print(f"VaultPath: {vault.getVaultPath()}")
vault.open()
vault.put("test-key", "test-value")
print(json.dumps(vault.getEncodedVault(), indent=4))
vault.close()

