
import json
import os

from .openvault_impl import OpenVault

class FileVault(OpenVault):
	def __init__(self, encoderInstance, options):
		OpenVault.__init__(self, encoderInstance)

		self._vault_dir = options.get("vaultdir", None)
		self._vault_path = os.path.join(_vault_dir, ".database.json")
		
	def _read(self):
		if os.path.exits(self._vault_path):
			f = open(self._vault_path, "r")
			content = f.read()
			f.close()
			return content
		return None

	def _write(self, content):
		d = os.path.dirname(self._vault_path)
		if not os.path.exists(d):
			os.makedirs(d)
		f = open(self._vault_path, "w")
		f.write(content)
		f.close()

	def getVaultPath(self):
		return self._vault_path

	def open(self):
		content = self._read()
		if content != None:
			encoded_vault = json.loads(content)
			self._vault = { k : self._encoder.decode(k, v) for k, v in encoded_vault.items()}
		else:
			self._vault = {}
		
	def close(self) -> bool:
		if OpenVault.close(self):
			encoded_vault = self.getEncodedVault()
			self._write(json.dumps(encoded_vault, indent=2))
			return True

		return False

	

