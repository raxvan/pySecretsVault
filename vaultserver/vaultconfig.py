
import os
import sys
import time
from shared_memory_dict import SharedMemoryDict
import secretsvault

NAME = os.environ.get("VAULT_NAME", 'vn')
CONFIG_FOLDER = os.environ.get("VAULT_CONFIG_DIR", '/vault/config')

CONFIG_STORAGE = secretsvault.CreateFileStorage(CONFIG_FOLDER, False)
ENCODER = secretsvault.CreateEncoder(CONFIG_STORAGE, False) #this can never be True
if ENCODER == None:
	raise Exception("Failed to create encoder!")
CONFIG_STORAGE.clear()
config = SharedMemoryDict(name=f'{NAME}Config', size=2048)
pn, pk = ENCODER.get_private_key()

config[pn] = pk

try:
	print("holding on ...")
	while True:
		time.sleep(5)  # Sleep for 1 second to reduce CPU usage
except KeyboardInterrupt:
	pass