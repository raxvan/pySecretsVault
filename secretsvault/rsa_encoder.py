import os
import base64
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

	def get_public_key(self) -> str:
		pem = self.public_key.public_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PublicFormat.SubjectPublicKeyInfo
		)
		return pem.decode('utf-8')

	def get_private_key(self) -> str:
		pem = self.private_key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption()
		)
		return pem.decode('utf-8')

	def init_with_private_key(self, pemstr : str):
		self.private_key = serialization.load_pem_private_key(
			pemstr.encode('utf-8'),
			password=None,
		)
		self.public_key = self.private_key.public_key()

	def init_with_public_key(self, pemstr : str):
		self.public_key = serialization.load_pem_public_key(
			pemstr.encode('utf-8'),
		)
		self.private_key = None

	def canEncode(self):
		return self.public_key != None

	def canDecode(self):
		return self.private_key != None

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
		return base64.b64encode(encrypted).decode('ascii')

	def decode(self, key: str, value: str) -> str:
		decrypted = self.private_key.decrypt(
			base64.b64decode(value.encode("ascii")),
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
		return decrypted.decode('utf-8')

	