
import secretsvault
import sys

CONFIG_STORAGE = secretsvault.CreateFileStorage(sys.argv[1], False)
secretsvault.WaitForPublicKey(CONFIG_STORAGE)
