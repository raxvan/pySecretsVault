from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import os
import json
import base64

def vault_rsa_encrypt(public_key, message):
	encrypted = public_key.encrypt(
		message,
		rsa_padding.OAEP(
			mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return encrypted

def vault_rsa_decrypt(private_key, encrypted_message):
	decrypted = private_key.decrypt(
		encrypted_message,
		rsa_padding.OAEP(
			mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return decrypted

def vault_aes_encrypt(key, iv, plaintext):
	padder = padding.PKCS7(algorithms.AES.block_size).padder()
	padded_data = padder.update(plaintext) + padder.finalize()
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	encryptor = cipher.encryptor()
	encrypted = encryptor.update(padded_data) + encryptor.finalize()
	return encrypted

def vault_aes_decrypt(key, iv, encrypted_data):
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
	decryptor = cipher.decryptor()
	padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
	unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
	plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
	return plaintext

def vault_encrypt_message(public_key, plaintext):
	salt = os.urandom(16)
	iv = os.urandom(16)
	aes_key = os.urandom(32)
	
	header = salt + iv + aes_key #+ base64.b64encode(json.dumps(payload).encode('ascii'))
	encrypted_header = vault_rsa_encrypt(public_key, header)
	
	encrypted_data = vault_aes_encrypt(aes_key, iv, plaintext.encode())
	return encrypted_header + encrypted_data

def vault_decrypt_message(private_key, encrypted_message):
	encrypted_header = encrypted_message[:256]
	encrypted_data = encrypted_message[256:]

	decrpyted_header = vault_rsa_decrypt(private_key, encrypted_header)

	salt = decrpyted_header[0:16]
	iv = decrpyted_header[16:32]
	aes_key = decrpyted_header[32:64]
	#payload = decrpyted_header[64:]

	plaintext = vault_aes_decrypt(aes_key, iv, encrypted_data)

	return plaintext.decode()