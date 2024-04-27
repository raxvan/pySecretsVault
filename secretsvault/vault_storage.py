import os

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

def _create_path(abs_static_path, item):
	full_path = os.path.join(abs_static_path, item)
	normalized_path = os.path.normpath(full_path)
	if not normalized_path.startswith(os.path.abspath(abs_static_path) + os.sep):
		return None
	return normalized_path

def _delete_files_in_folder(folder_path):
	if not os.path.isdir(folder_path):
		raise Exception(f"Error: The provided path '{folder_path}' is not a valid directory.")

	for filename in os.listdir(folder_path):
		file_path = os.path.join(folder_path, filename)
		
		# Check if it is a file and not a directory
		if os.path.isfile(file_path):
			try:
				os.remove(file_path)  # Remove the file
			except Exception as e:
				raise Exception(f"Failed to delete {file_path}. Reason: {e}")



class FileStorageMap():
	def __init__(self, basedir, isbinary):
		self.folder = os.path.abspath(basedir)
		self.isbinary = isbinary

		os.makedirs(self.folder, exist_ok=True)

	def _write_file(self, name, content):
		fp = _create_path(self.folder, name)
		if(fp == None):
			return

		f = open(fp, "wb" if self.isbinary else "w")
		f.write(content)
		f.close()

	def _read_file(self, name : str) -> bytes:
		fp = _create_path(self.folder, name)
		if fp == None or os.path.exists(fp) == False:
			return None

		try:
			f = open(fp, "rb" if self.isbinary else "r")
			content = f.read()
			f.close()
			return content
		except:
			return None

	def clear(self):
		_delete_files_in_folder(self.folder)

	def keys(self):
		return os.listdir(self.folder)

	def get(self, key, default):
		c = self._read_file(key)
		if c != None:
			return c
		return default

	def __getitem__(self, key):
		return self._read_file(key)

	def __setitem__(self, key, value):
		self._write_file(key, value)




# class FileStorage():
# 	def __init__(self, userDir):
# 		self.baseFolder = os.path.abspath(userDir)
# 		self.configFolder = os.path.join(self.baseFolder, 'config')
# 		self.mapFolder = os.path.join(self.baseFolder, 'data')

# 		os.makedirs(self.configFolder, exist_ok=True)
# 		os.makedirs(self.mapFolder, exist_ok=True)

# 	def getConfigPath(self):
# 		return self.configFolder

# 	def getDataPath(self):
# 		return self.mapFolder

# 	def getBasePath(self):
# 		return self.baseFolder

# 	def _write_file(self, abspath, content, mode):
# 		fp = os.path.join(abspath, item)
# 		f = open(fp, mode)
# 		f.write(content)
# 		f.close()

# 	def _read_file(self, abspath, mode) -> bytes:
# 		if not os.path.exists(abspath):
# 			return None
# 		try:
# 			f = open(abspath, mode)
# 			content = f.read()
# 			f.close()
# 			return content
# 		except:
# 			return None

# 	def writeConfig(self, item, content : str):
# 		self._write_file(os.path.join(self.configFolder, item), content, "w")

# 	def readConfig(self, item) -> str:
# 		return self._read_file(os.path.join(self.configFolder, item), "r")


# 	def write(self, item, content : bytes):
# 		self._write_file(os.path.join(self.mapFolder, item), content, "wb")

# 	def read(self, item) -> bytes:
# 		return self._read_file(os.path.join(self.mapFolder, item), "rb")


