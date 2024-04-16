
import os
import sys
import base64

from .vault_folder import GetVaultDirectory


def CreateOptions(**kwargs):
	vault_folder = GetVaultDirectory(kwargs.get("vaultdir", None))

	return {
		"vaultdir" : vault_folder
	}

def CreateRsaEncoder(options):
	from .rsa_encoder import RsaEncoder

	e = RsaEncoder(options)

	return e

def CreateFileVault(encoder, options):
	from .secretsvault_impl import FileVault

	if "vaultdir" not in options:
		raise Exception("Mising option, vault directory path (vaultdir).")

	return FileVault(encoder, options)

def details():
	import cryptography

	v = {
		"version" : "0.0.1",
		"url" : "https://github.com/raxvan/pysecrets-vault",
		"cryptography-versin" : cryptography.__version__,
	}

	return v