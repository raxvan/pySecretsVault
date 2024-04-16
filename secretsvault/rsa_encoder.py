import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class RsaEncoder():
	def __init__(self, options):
		self.public_key = None
		self.private_key = None

	def generate_keys(self):
		private_key = rsa.generate_private_key(
			public_exponent=65537,
			key_size=2048,
			backend=default_backend()
		)
		public_key = private_key.public_key()
		
		self.public_key = public_key
		self.private_key = private_key

	def get_public_key(self):
		pass

	def get_private_key(self):
		pass

	def encode(self, key: str, value: str) -> str:
		message_bytes = value.encode('utf-8')
		encrypted = self.public_key.encrypt(
			message_bytes,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
		return encrypted

	def decode(self, key: str, value: str) -> str:
		decrypted = self.private_key.decrypt(
			value,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
		return decrypted.decode('utf-8')

	