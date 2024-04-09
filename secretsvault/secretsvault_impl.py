
import os
import json

_hidden_dir = ".vault"

def GetVaultDirectory():
	envloc = os.environ.get("SECRETSVAULT", None)
	if envloc != None:
		return envloc

	start_dir = os.path.abspath(os.getcwd())

	current_dir = start_dir
	while True:
		vaultpath = os.path.join(current_dir, _hidden_dir)
		if os.path.isdir(vaultpath):
			return vaultpath

		parent_dir = os.path.dirname(current_dir)
		if parent_dir == current_dir:
			break
		current_dir = parent_dir

	return os.path.join(start_dir,_hidden_dir)

class Vault():
	def __init__(self, encoderInstance, vaultPath = None):
		
		self._vault = None
		self._dirty = False
		self._encoder = encoderInstance

		if vaultPath != None:
			self._vault_path = vaultPath
		else:
			self._vault_path = os.path.join(GetVaultDirectory(), "vault.json")
		
	def _read(self):
		if(os.path.exits(self._vault_path)):
			f = open(self._vault_path, "r")
			content = f.read()
			f.close()
			return f
		return {}

	def _write(self, content):
		d = os.path.dirname(self._vault_path)
		if not os.path.exists(d):
			os.makedirs(d)
		f = open(self._vault_path, "w")
		f.write(content)
		f.close()

	def getVaultPath(self):
		return self._vault_path

	def getEncodedVault(self):
		return { k : self._encoder.encode(k, v) for k, v in self._vault.items()}

	def open(self):
		if os.path.exists(self._vault_path):
			encoded_vault = json.loads(self._get_file_contents())
			self._vault = { k : self._encoder.decode(k, v) for k, v in encoded_vault.items()}

		self._vault = {}
		
	def close(self) -> bool:
		if self._dirty:
			self._dirty = False
			encoded_vault = self.getEncodedVault()
			self._write(json.dumps(encoded_vault, indent=2))
			return True

		return False

	def put(self, key : str, value : str):
		self._dirty = True
		self._vault[key] = value

	def get(self, key : str, default : str) -> str:
		return self._vault.get(key, default)

	def format(self, s : str) -> str:
		return s.format(**self._vault)

