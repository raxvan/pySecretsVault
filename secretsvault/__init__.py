
import os
import sys
import base64

def CreateEncoder(storage):
	from .rsa_encoder import RsaEncoder
	return RsaEncoder(storage)

def CreateVault(encoder, storage):
	from .vault_impl import Vault
	return Vault(encoder, storage)

def CreateFileStorage(userPath = None):
	from .vault_storage import FileStorage

	return FileStorage(userPath)


def details():
	import cryptography

	v = {
		"version" : "0.0.1",
		"url" : "https://github.com/raxvan/pysecrets-vault",
		"cryptography-versin" : cryptography.__version__,
	}

	return v