
import json
import os

class OpenVault():
	def __init__(self, encoderInstance):
		self._vault = None
		self._dirty = False
		self._encoder = encoderInstance

	def open(self):
		self._dirty = False
		
	def close(self) -> bool:
		if self._dirty:
			self._dirty = False
			return True

		return False 

	def isOpen(self) -> bool:
		return self._vault != None

	def _drop(self):
		self._vault = None
		self._dirty = False

	def getEncodedVault(self):
		return { k : self._encoder.encode(k, v) for k, v in self._vault.items()}

	def put(self, key : str, value : str):
		self._vault[key] = value
		self._dirty = True

	def get(self, key : str, default : str = None) -> str:
		return self._vault.get(key, default)

	def format(self, s : str) -> str:
		return s.format(**self._vault)


