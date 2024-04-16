
import json
import os

class Vault():
	def __init__(self, encoderInstance):
		self._dirty = None
		self._encoded = None

		self._vault = None
		self._encoder = encoderInstance

	def create(self, encoded : bool, vault : dict):
		self._dirty = False
		self._encoded = encoded
		
		self._vault = vault

	def destroy(self):
		self._vault = None
		
	def isDirty(self) -> bool:
		return self._dirty

	def isOpen(self) -> bool:
		return self._vault != None

	def isEncoded(self) -> bool:
		return self._encoded

	def getEncoded(self):
		if self._encoded:
			return self._vault
		return { k : self._encoder.encode(k, v) for k, v in self._vault.items()}

	def getDecoded(self):
		if self._encoded:
			return { k : self._encoder.decode(k, v) for k, v in self._vault.items()}
		return self._vault

	def put(self, key : str, value : str):
		self._dirty = True

		if self._encoded:
			self._vault[key] = self._encoder.encode(key, vault)
		else:
			self._vault[key] = value

	def putEnc(self, key : str, encoded_value : str):
		self._dirty = True

		if self._encoded:
			self._vault[key] = encoded_value
		else:
			self._vault[key] = self._encoder.encode(key, encoded_value)


	def get(self, key : str, default_value : str = None) -> str:
		kv = self._vault.get(key, None)
		if kv == None:
			return default_value
		if self._encoded:
			return self._encoder.decode(key, kv)
		return kv

	def format(self, s : str) -> str:
		vault = self.getDecoded()
		return s.format(**vault)

	def open(self):
		pass

	def close(self):
		pass

