
import os
import sys
import json

#_this_dir = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.join(_this_dir,".."))

import secretsvault

print(json.dumps(secretsvault.details(), indent = 4))

enc = secretsvault.CreateRsaEncoder({})

enc.generate_keys() #generate a key pair

public_key = enc.get_public_key()
private_key = enc.get_private_key()

print(f"public key:\n{public_key}")
print(f"private key:\n{private_key}")

vault = secretsvault.CreateFileVault(enc, {})

#open close
assert(vault.isOpen() == False)
assert(vault.open() == False) #false because the vault does not exists, it's going to be created
assert(vault.isOpen() == True)
vault.put("test-key", "test-value")
assert(vault.close() == True)
assert(vault.isOpen() == False)


#open print
assert(vault.open() == True) #because it exists
print(json.dumps(vault.getEncodedVault(), indent=4))
assert(vault.get("test-key") == "test-value")
assert(vault.format("{test-key}") == "test-value")


#test public key only
enc.init_with_public_key(public_key)
assert(enc.canDecode() == False)
vault.put("test-key2", "test-value2")
vault.close()

assert(vault.open() == False) #should not be able to decode
assert(vault.isOpen() == False)

enc.init_with_private_key(private_key)
assert(enc.canDecode() == True)
assert(enc.canDecode() == True)
assert(vault.open() == True) #should not be able to decode
assert(vault.get("test-key2") == "test-value2")
vault.close()