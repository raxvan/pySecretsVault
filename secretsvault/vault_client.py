
import requests
import json
import os

from .vault_encoder import CreateEncoderWith
from .vault_encoder import CreateNewEncoder

_timeout = 2 #2 sec

_hidden_dir = ".vault"
_envvar = "VAULT_CLIENT_CONFIG"

def _check_home_folder():
	home_directory = os.path.expanduser('~')
	folder = os.path.join(home_directory, _hidden_dir)
	
	if os.path.exists(folder) and os.path.isdir(folder):
		return os.path.abspath(folder)
	return None

def FindVaultConfigImpl(userSearchDir):
	folder = os.environ.get(_envvar, None)
	if folder != None:
		if os.path.exists(folder) and os.path.isdir(folder):
			return folder

	#if userSearchDir != None:
	#	folder = os.path.join(userSearchDir, _hidden_dir)
	#	if os.path.exists(folder):
	#		user_path = os.path.abspath(folder)
	#		return user_path

	folder = _check_home_folder()
	if folder != None:
		return folder

	folder = os.path.abspath(userSearchDir)

	current_dir = folder
	while True:
		vaultpath = os.path.join(current_dir, _hidden_dir)
		if os.path.exists(vaultpath) and os.path.isdir(vaultpath):
			return vaultpath

		parent_dir = os.path.dirname(current_dir)
		if parent_dir == current_dir:
			break
		current_dir = parent_dir

	return os.path.join(folder, _hidden_dir)


def CreateVaultImpl(config):
	url = config.get('url', None)
	if url != None:
		return RemoteVault(url, config)


class ApiMap():
	def __init__(self, url):
		self.apiExec = f"{url}/exc"
		self.apiInfo = f"{url}/info"
		self.apiUnlock = f"{url}/unlock"


class RemoteVault(ApiMap):
	#handler for flask_server.py implementation

	def __init__(self, url, desc):
		ApiMap.__init__(self, url)
		self.timeout = desc.get("timeout", _timeout)

		#init
		self.vaultEncoder = CreateEncoderWith(desc, False)
		if self.vaultEncoder == None:
			self.vaultEncoder = CreateEncoderWith(self.info(), False)
			if (self.vaultEncoder == None):
				raise Exception(f"Failed to create vault encoder with {url}")

		self.upstreamEncoder = CreateNewEncoder()
		self.publicData = self.upstreamEncoder.get_public_data()

	def unlock(self):
		try:
			response = requests.get(self.apiUnlock, timeout=self.timeout)
			if response.status_code != 200:
				raise Exception(f"Request {self.apiInfo} failed with code {response.status_code}:\n{response.text}");
			
		except Exception as e:
			raise Exception(f"Request {self.apiUnlock} failed!\n{str(e)}")

		return True			

	def info(self):
		try:
			response = requests.get(self.apiInfo, timeout=self.timeout)
			if response.status_code != 200:
				raise Exception(f"Request {self.apiInfo} failed with code {response.status_code}:\n{response.text}");
			content = response.text
			return json.loads(content)
		except Exception as e:
			raise Exception(f"Request {self.apiInfo} failed!\n{str(e)}")

	def _execute(self, operation):

		operation.update(self.publicData)

		packet = self.vaultEncoder.encodeStr(json.dumps(operation))

		headers = {'Content-Length': str(len(operation))}

		try:
			response = requests.post(self.apiExec, headers=headers, data=packet)
			if response.status_code != 200:
				raise Exception(f"Request {self.apiInfo} failed with code {response.status_code}:\n{response.text}");
			reply = self.upstreamEncoder.decodeStr(response.content)
			return json.loads(reply)
		except Exception as e:
			raise Exception(f"Request {self.apiExec} failed!\n{str(e)}")

	def keys(self, regex = ""):
		result = self._execute({
			"list" : regex
		})
		return result['list']

	def query(self, items_list):
		result = self._execute({
			"query" : items_list
		})
		return result['query']

	def __getitem__(self, key):
		result = self._execute({
			"query" : [key]
		})
		return result['query'].get(key, None)

	def __setitem__(self, key, value):
		result = self._execute({
			"set" : {
				key : value
			}
		})
		return result['set'] == 1


	
		


	