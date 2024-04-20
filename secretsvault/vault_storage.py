import os
import json

_hidden_dir = ".vault"
_envvar = "SECRETSVAULT"

def _check_home_folder():
	home_directory = os.path.expanduser('~')
	folder = os.path.join(home_directory, _hidden_dir)
	
	if os.path.exists(folder) and os.path.isdir(folder):
		return os.path.abspath(folder)
	return None

def GetVaultDirectory(userPath):
	folder = os.environ.get(_envvar, None)
	if folder != None:
		return folder

	if userPath != None:
		folder = os.path.join(userPath, _hidden_dir)
		if os.path.exists(folder):
			user_path = os.path.abspath(folder)
			return user_path

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

class FileStorage():
	def __init__(self, userDir):
		self.folder = GetVaultDirectory(userDir)

	def get_location(self):
		return self.folder

	def writeJson(self, item, content):
		if not os.path.exists(self.folder):
			os.makedirs(self.folder)

		fp = os.path.join(self.folder, item)
		f = open(fp, "w")
		f.write(json.dumps(content, indent = 2))
		f.close()

	def readJson(self, item):
		fp = os.path.join(self.folder, item)

		if not os.path.exists(fp):
			return None

		try:
			f = open(fp, "r")
			content = json.load(f)
			f.close()
			return content
		except:
			return None

	def writeStr(self, item, content):
		if not os.path.exists(self.folder):
			os.makedirs(self.folder)

		fp = os.path.join(self.folder, item)
		f = open(fp, "w")
		f.write(content)
		f.close()

	def readStr(self, item):
		fp = os.path.join(self.folder, item)

		if not os.path.exists(fp):
			return None

		try:
			f = open(fp, "r")
			content = f.read()
			f.close()
			return content
		except:
			return None
