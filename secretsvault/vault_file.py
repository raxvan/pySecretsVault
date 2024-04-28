
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from base64 import b64encode, b64decode

import os

def _aes_encrypt(key, iv, plaintext):
	padder = padding.PKCS7(algorithms.AES.block_size).padder()
	padded_data = padder.update(plaintext) + padder.finalize()
	#iv = os.urandom(16)
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	encryptor = cipher.encryptor()
	encrypted = encryptor.update(padded_data) + encryptor.finalize()
	return iv + encrypted

def _aes_decrypt(key, iv, encrypted_data : bytes):
	iv = encrypted_message[:16]
	encrypted_data = encrypted_message[16:]
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	decryptor = cipher.decryptor()
	padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
	unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
	plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
	return plaintext
