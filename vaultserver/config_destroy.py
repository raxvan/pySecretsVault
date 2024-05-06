
import secretsvault
import sys
import os
import time

time.sleep(int(sys.argv[1]))
CONFIG_STORAGE = secretsvault.CreateFileStorage(sys.argv[2], False)
CONFIG_STORAGE.clear()

