
import os
import sys
import json

import secretsvault

class TestStorage():
	def __init__(self):
		self.data = {}

	def readConfig(self, k):
		return self.data.get(k,None)

	def writeConfig(self, k, c):
		self.data[k] = c

	def removeData(self, k):
		self.data[k] = None

def test_encoder(): 
	ts = {}
	enc1 = secretsvault.CreateEncoder(ts, True)
	enc1.serialize(ts)

	print("Storage:")
	print(json.dumps(ts,indent=4))

	enc2 = secretsvault.CreateEncoder(ts, False)
	assert(enc2 != None)

	s1 = enc1.encodeStr("test-value1")
	assert(enc2.decodeStr( s1) == "test-value1")

	s2 = enc2.encodeStr("test-value2")
	assert(enc1.decodeStr(s2) == "test-value2")
	
def test_vault():
	vaultConfig = {
		"url":"http://127.0.0.1:5000",
	}
	
	v = secretsvault.CreateVault(vaultConfig)

	inf1 = v.info()
	print("Vault Info:")
	print(json.dumps(inf1, indent=4))
	
	#test getters/setters
	v["test-key"] = "test-value"
	assert(v["test-key"] == "test-value")

	assert("test-key" in v.keys()) 


def main():
	test_encoder()
	test_vault()

main()
