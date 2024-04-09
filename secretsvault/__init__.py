
import os
import sys
import base64

from .secretsvault_impl import Vault

def _create_fernet(cypher_salt : str, key: str):
	
	from cryptography.fernet import Fernet
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

	kdf = Scrypt(
		salt=cypher_salt.encode("ascii"),
		length=32,
		n=2**14,
		r=8,
		p=1,
		backend=default_backend()
	)
	_fk = base64.urlsafe_b64encode(kdf.derive(key.encode("ascii")))
	return Fernet(_fk)

class FernetEncoder():
	def __init__(self, salt):
		self.salt = salt

	def encode(self, key: str, value: str) -> str:
		f = _create_fernet(self.salt, key)
		encrypted_data = f.encrypt(value.encode('utf-8'))
		return base64.b64encode(encrypted_data).decode("ascii")

	def decode(self, key: str, value: str) -> str:
		f = _create_fernet(self.salt, key)
		return f.decrypt(value).decode('utf-8')

	def encodeBuffer(self, value : bytes) -> str:
		encrypted_data = self.api.encrypt(value)
		return base64.b64encode(encrypted_data).decode("ascii")

	def decodeBuffer(self, value : str) -> bytes:
		raw_data = base64.b64decode(encrypted_string.encode("ascii"))
		return self.api.decrypt(raw_data)

def CreateFernetEncoder(cypher_salt : str) -> FernetEncoder:
	return FernetEncoder(cypher_salt)

def details():
	import cryptography

	v = {
		"version" : "0.0.1",
		"url" : "https://github.com/raxvan/pysecrets-vault",
		"cryptography-versin" : cryptography.__version__,
	}

	return v