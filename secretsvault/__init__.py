
import os
import sys
import base64

from .vault_folder import GetVaultDirectory

def CreateRsaEncoder(options):
	from .rsa_encoder import RsaEncoder

	e = RsaEncoder(options)

	return e

def CreateFileVault(encoder, options):
	from .vault_file_impl import FileVault

	vault_folder = GetVaultDirectory(options.get("vaultdir", None))

	return FileVault(encoder, vault_folder)

def details():
	import cryptography

	v = {
		"version" : "0.0.1",
		"url" : "https://github.com/raxvan/pysecrets-vault",
		"cryptography-versin" : cryptography.__version__,
	}

	return v