
import os
import json

_hidden_dir = ".vault"

def _check_home_folder():
	# Get the path to the user's home directory
	home_directory = os.path.expanduser('~')
	folder = os.path.join(home_directory, _hidden_dir)
	
	# Check if the folder exists
	if os.path.exists(folder) and os.path.isdir(folder):
		return folder
	return None


def GetVaultDirectory():
	folder = os.environ.get("SECRETSVAULT", None)
	if folder != None:
		return folder

	folder = _check_home_folder()
	if folder != None:
		return folder

	folder = os.path.abspath(os.getcwd())

	current_dir = folder
	while True:
		vaultpath = os.path.join(current_dir, _hidden_dir)
		if os.path.exists(vaultpath) and os.path.isdir(vaultpath):
			return vaultpath

		parent_dir = os.path.dirname(current_dir)
		if parent_dir == current_dir:
			break
		current_dir = parent_dir

	return os.path.join(folder,_hidden_dir)

class Vault():
	def __init__(self, encoderInstance, vaultFolder = None):
		
		self._vault = None
		self._dirty = False
		self._encoder = encoderInstance

		if vaultFolder != None:
			self._vault_path = vaultFolder
		else:
			self._vault_path = os.path.join(GetVaultDirectory(vaultFolder), "vault.json")
		
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

