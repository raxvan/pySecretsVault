import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

_public_key = "PublicKey"
_private_key = "PrivateKey"

def CreateEncoderWith(data, createNew):
	decode_key = data.get(_private_key, None)
	if decode_key != None:
		result = RsaEncoder()
		result.load_private(decode_key)
		return result

	encode_key = data.get(_public_key, None)
	if encode_key != None:
		result = RsaEncoder()
		result.load_public(encode_key)
		return result

	if createNew:
		result = RsaEncoder()
		result.create()
		return result

	return None

def CreateNewEncoder():
	result = RsaEncoder()
	result.create()
	return result

def InspectDataForKeys(data):
	#returns:
	# True : if encoder can pe decode
	# False : if encode can only encode
	# None : if encoder can't be created
	decode_key = data.get(_private_key, None)
	if decode_key != None:
		return True
	encode_key = data.get(_public_key, None)
	if encode_key != None:
		return False

	return None


class RsaEncoder():
	def __init__(self):
		self.privateKey = None
		self.publicKey = None

	def create(self):
		k = rsa.generate_private_key(
			public_exponent=65537,
			key_size=2048,
			backend=default_backend()
		)
		self.privateKey = k
		self.publicKey = k.public_key()

	def serialize(self, out, private = True):
		if self.privateKey != None and private == True:
			pb = self.privateKey.private_bytes(
				encoding=serialization.Encoding.DER,
				format=serialization.PrivateFormat.PKCS8,
				encryption_algorithm=serialization.NoEncryption()
			)
			out[_private_key] = base64.b64encode(pb).decode('ascii')
		elif self.publicKey != None:
			pb = self.publicKey.public_bytes(
				encoding=serialization.Encoding.DER,
				format=serialization.PublicFormat.SubjectPublicKeyInfo
			)
			out[_public_key] = base64.b64encode(pb).decode('ascii')

	def load_private(self, pk : str):
		key_bytes = base64.b64decode(pk.encode("ascii"))
		self.privateKey = serialization.load_der_private_key(
			key_bytes,
			password=None
		)
		self.publicKey = self.privateKey.public_key()

	def load_public(self, pk : str):
		key_bytes = base64.b64decode(pk.encode("ascii"))
		self.privateKey = None
		self.publicKey = serialization.load_der_public_key(
			key_bytes
		)

	def get_public_data(self) -> str:
		pb = self.publicKey.public_bytes(
			encoding=serialization.Encoding.DER,
			format=serialization.PublicFormat.SubjectPublicKeyInfo
		)
		return {
			_public_key : base64.b64encode(pb).decode('ascii')
		}

	def canDecode(self):
		return self.privateKey != None

	def encodeStr(self, value: str) -> bytes:
		message_bytes = value.encode('utf-8')
	
		encrypted = self.publicKey.encrypt(
			message_bytes,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
		return encrypted

		#return base64.b64encode(encrypted).decode('ascii')

	def decodeStr(self, value: bytes) -> str:
		decrypted = self.privateKey.decrypt(
			value,
			#base64.b64decode(value.encode("ascii")),
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
		return decrypted.decode('utf-8')


