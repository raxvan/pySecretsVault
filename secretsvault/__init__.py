
import os
import sys
import base64

from .vault_encoder import CreateNewEncoder
from .vault_encoder import CreateEncoder
from .vault_encoder import InspectDataForKeys

from .vault_utils import vault_encode_file
from .vault_utils import vault_decode_file
from .vault_utils import vault_encode_str
from .vault_utils import vault_decode_str



def CreateFileStorage(userPath, isbinary):
	from .vault_storage import FileStorageMap
	return FileStorageMap(userPath, isbinary)

def CreateVault(desc):
	from .vault_client import CreateVaultImpl
	return CreateVaultImpl(desc)

def CreateVault(desc):
	from .vault_client import CreateVaultImpl
	return CreateVaultImpl(desc)

def GetRemoteInfo(url, timeout):
	from .vault_client import GetRemoteInfoImpl
	return GetRemoteInfoImpl(url, timeout)

def OpenVault():
	url = os.environ.get("VAULT_URL", None)
	if url == None:
		raise Exception("No url provided (VAULT_URL)")

	v = CreateVault({
		"url" : url
	})
	if v == None:
		raise Exception("Could not load vault!")

	if v.ready():
		items = v.query(["url", "PublicKey"])
		if len(items) == 2:
			return CreateVault(items)

	return v



def WaitForPublicKey(data):
	from .vault_encoder import ConfigWaitForPublicKey
	ConfigWaitForPublicKey(data)

def details():
	from ._version import __version__
	import cryptography

	v = {
		"cryptography-version" : cryptography.__version__,
		"version" : __version__,
	}

	return v