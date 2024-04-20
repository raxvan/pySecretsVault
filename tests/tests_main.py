
import os
import sys
import json

#_this_dir = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.join(_this_dir,".."))

import secretsvault

print(json.dumps(secretsvault.details(), indent = 4))

storage = secretsvault.CreateFileStorage()
enc = secretsvault.CreateEncoder()
vault = secretsvault.CreateVault(enc, storage)

#generate encoder keys
enc.generate_keys() #generate a key pair
enc.save(storage, True)

public_key = enc.get_public_key()
private_key = enc.get_private_key()

print(f"vault folder:\n{storage.folder}")
print(f"public key:\n{public_key}")
print(f"private key:\n{private_key}")

#open close
assert(vault.isOpen() == False)
assert(vault.open(False) == False) #false because the vault does not exists, it's going to be created
assert(vault.isOpen() == True)
assert(vault.isEncoded() == False)
vault.set("test-key", "test-value")
assert(vault.close() == True)
assert(vault.isOpen() == False)


#open print
assert(vault.open(False) == True) #because it exists
print(json.dumps(vault.getContent(), indent=4))
assert(vault.get("test-key") == "test-value")
assert(vault.format("{test-key}") == "test-value")
vault.close()

enc.init_with_public_key(public_key)

assert(vault.open(True) == True)
assert(enc.canDecode() == False)
vault.set("test-key2", "test-value2")
print(json.dumps(vault.getContent(), indent=4))
vault.close()

assert(vault.open(False) == False) #should not be able to decode
vault.destroy()

enc.init_with_private_key(private_key)
assert(enc.canDecode() == True)
assert(enc.canDecode() == True)
assert(vault.open(True) == True)
assert(vault.get("test-key2") == "test-value2")
vault.close()