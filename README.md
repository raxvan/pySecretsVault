
# pysecrets-vault

For secrets management. This package manages key/value pairs where the value is encoded.

# Quick start

```
storage = secretsvault.CreateFileStorage()
enc = secretsvault.CreateEncoder(storage)
vault = secretsvault.CreateVault(enc, storage)

# to create a public/private key pair you can use:
enc.generate_keys() #generate a key pair
enc.save(True) #save the keys into the storage so that initialize() can read them

# from this point you need to open the vault, operate on values, and close the vault:

vault.open()
vault.set("my-key", "my-value")
vault.close()

# the vault file stores the key and encrypted value
```

