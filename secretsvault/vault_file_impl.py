
import json
import os

from .vault_base_impl import Vault

class FileVault(Vault):
	def __init__(self, encoderInstance, vaultdir):
		Vault.__init__(self, encoderInstance)

		self._vault_dir = vaultdir
		self._vault_path = os.path.join(vaultdir, ".database.json")
		
	def _read(self):
		if os.path.exists(self._vault_path):
			f = open(self._vault_path, "r")
			content = f.read()
			f.close()
			return content
		return None

	def _write(self, content : str):
		d = os.path.dirname(self._vault_path)
		if not os.path.exists(d):
			os.makedirs(d)
		f = open(self._vault_path, "w")
		f.write(content)
		f.close()

	def getVaultPath(self):
		return self._vault_path

	def open(self):
		if self._encoder.canDecode() == False:
			return False
		content = self._read()
		if content != None:
			encoded_vault = json.loads(content)
			Vault.create(self, False, { k : self._encoder.decode(k, v) for k, v in encoded_vault.items()})
			return True
		else:
			Vault.create(self, False, {})
			return False
		
	def close(self) -> bool:
		if self._encoder.canEncode() == False:
			return False
		
		if Vault.isDirty(self):
			encoded_vault = self.getEncoded()
			self._write(json.dumps(encoded_vault, indent=2))
			self.destroy()
			return True

		return False

	

