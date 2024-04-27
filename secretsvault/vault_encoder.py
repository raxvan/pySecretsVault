import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

_public_key = "PublicKey"
_private_key = "PrivateKey"

################################################################################################

def CreateEncoderWith(data, createNew):
	decode_key = data.get(_private_key, None)
	if decode_key != None:
		result = EncoderImpl()
		result.load_private(decode_key)
		return result

	encode_key = data.get(_public_key, None)
	if encode_key != None:
		result = EncoderImpl()
		result.load_public(encode_key)
		return result

	if createNew:
		result = EncoderImpl()
		result.create()
		return result

	return None

def CreateNewEncoder():
	result = EncoderImpl()
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

################################################################################################

def _rsa_encrypt(public_key, message):
	"""Encrypt message using RSA public key."""
	encrypted = public_key.encrypt(
		message,
		rsa_padding.OAEP(
			mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return encrypted

def _rsa_decrypt(private_key, encrypted_message):
	decrypted = private_key.decrypt(
		encrypted_message,
		rsa_padding.OAEP(
			mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return decrypted

def _aes_encrypt(key, plaintext):
	padder = padding.PKCS7(algorithms.AES.block_size).padder()
	padded_data = padder.update(plaintext) + padder.finalize()
	iv = os.urandom(16)
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	encryptor = cipher.encryptor()
	encrypted = encryptor.update(padded_data) + encryptor.finalize()
	return iv + encrypted

def _aes_decrypt(key, encrypted_message):
	iv = encrypted_message[:16]
	encrypted_data = encrypted_message[16:]
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	decryptor = cipher.decryptor()
	padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
	unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
	plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
	return plaintext

def _encrypt_message(public_key, plaintext):
	aes_key = os.urandom(32)
	encrypted_aes_key = _rsa_encrypt(public_key, aes_key)
	encrypted_data = _aes_encrypt(aes_key, plaintext.encode())
	return encrypted_aes_key + encrypted_data

def _decrypt_message(private_key, encrypted_message):
	encrypted_aes_key = encrypted_message[:256]
	encrypted_data = encrypted_message[256:]
	aes_key = _rsa_decrypt(private_key, encrypted_aes_key)
	plaintext = _aes_decrypt(aes_key, encrypted_data)
	return plaintext.decode()

################################################################################################

class EncoderImpl():
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
		return _encrypt_message(self.publicKey, value)

	def decodeStr(self, value: bytes) -> str:
		return _decrypt_message(self.privateKey, value)

