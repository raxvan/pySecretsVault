
import secretsvault
import sys

CONFIG_STORAGE = secretsvault.CreateFileStorage(sys.argv[1], False)
ENCODER = secretsvault.CreateEncoder(CONFIG_STORAGE, True)
ENCODER.serialize(CONFIG_STORAGE)
