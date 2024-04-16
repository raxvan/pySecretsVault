import os

_hidden_dir = ".vault"
_envvar = "SECRETSVAULT"

def _check_home_folder():
	home_directory = os.path.expanduser('~')
	folder = os.path.join(home_directory, _hidden_dir)
	
	if os.path.exists(folder) and os.path.isdir(folder):
		return folder
	return None


def GetVaultDirectory(userPath):
	folder = os.environ.get(_envvar, None)
	if folder != None:
		return folder

	if userPath != None and os.path.exists(userPath):
		user_path = os.path.abspath(userPath)
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


