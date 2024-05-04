
import os
import sys
import base64

from .vault_encoder import CreateEncoderWith
from .vault_encoder import InspectDataForKeys

from .vault_utils import vault_encode_file
from .vault_utils import vault_decode_file

def CreateEncoder(storage, createNew):
	return CreateEncoderWith(storage, createNew)

def CreateFileStorage(userPath, isbinary):
	from .vault_storage import FileStorageMap
	return FileStorageMap(userPath, isbinary)


def CreateVault(desc):
	from .vault_client import CreateVaultImpl
	return CreateVaultImpl(desc)

def CreateVault(desc):
	from .vault_client import CreateVaultImpl
	return CreateVaultImpl(desc)

def FindVaultConfigFolder(userPath):
	from .vault_client import FindVaultConfigImpl
	return FindVaultConfigImpl(userPath)


def details():
	import cryptography

	v = {
		"version" : "0.0.1",
		"url" : "https://github.com/raxvan/pysecrets-vault",
		"cryptography-version" : cryptography.__version__,
	}

	return v