
import json
import os

_database_entry = ".database.json"

class Vault():
	def __init__(self, encoderInstance, storageInstance):
		self._encoded = None
		self._dirty = None

		self._vault = None
		self._encoder = encoderInstance
		self._storage = storageInstance

	def create(self, encoded : bool, vault : dict):
		self._encoded = encoded
		self._dirty = False
		
		self._vault = vault

	def destroy(self):
		self._vault = None
		
	def isDirty(self) -> bool:
		return self._dirty

	def isOpen(self) -> bool:
		return self._vault != None

	def isEncoded(self) -> bool:
		return self._encoded

	def getContent(self) -> dict:
		return self._vault

	def getEncodedMap(self) -> dict:
		if self._encoded:
			return self._vault
		return { k : self._encoder.encode(k, v) for k, v in self._vault.items()}

	def getDecodedMap(self) -> dict:
		if self._encoded:
			return { k : self._encoder.decode(k, v) for k, v in self._vault.items()}
		return self._vault

	def set(self, key : str, value : str):
		self._dirty = True

		if self._encoded:
			self._vault[key] = self._encoder.encode(key, value)
		else:
			self._vault[key] = value

	def setEnc(self, key : str, encoded_value : str):
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

	def getEnc(self, key : str) -> str:
		kv = self._vault.get(key, None)
		if kv == None:
			return None
		if self._encoded:
			return kv
		else:
			return self._encoder.encode(key, kv)

	def format(self, s : str) -> str:
		vault = self.getDecodedMap()
		return s.format(**vault)

	def open(self, encoded = True):
		content = self._storage.readJson(_database_entry)
		if content != None:
			if encoded:
				Vault.create(self, True, content)
				return True
			elif self._encoder.canDecode():	
				Vault.create(self, False, { k : self._encoder.decode(k, v) for k, v in content.items()})
				return True
		
		Vault.create(self, False, {})
		return False
		
	def close(self, storage = None) -> bool:
		if self._encoder.canEncode() == False:
			return False
		
		if self.isDirty():
			encoded_vault = self.getEncodedMap()
			if storage != None:
				storage.writeJson(_database_entry,encoded_vault)
			else:
				self._storage.writeJson(_database_entry,encoded_vault)

			self.destroy()
			return True

		return False

	

