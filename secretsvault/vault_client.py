
import requests
import json
import os

from .vault_encoder import CreateEncoder
from .vault_encoder import CreateNewEncoder

_timeout = 2 #2 sec

def CreateVaultImpl(config):
	url = config.get('url', None)
	if url != None:
		return RemoteVault(url, config)

class ApiMap():
	def __init__(self, url):
		self.apiExec = f"{url}/exc"
		self.apiJoin = f"{url}/join"
		self.apiInfo = f"{url}/info"
		self.url = url

class RemoteVault(ApiMap):
	#handler for flask_server.py implementation

	def __init__(self, url, desc):
		ApiMap.__init__(self, url)
		self.timeout = desc.get("timeout", _timeout)

		#init
		self.vaultName = ""
		self.vaultEncoder = None

		self._init(desc)
		if self.vaultEncoder == None:
			self._init(self._join())

		self.upstreamEncoder = CreateNewEncoder()
		kn, kv = self.upstreamEncoder.get_public_key()
		self.publicKey = {
			kn : kv
		} 

	def _join(self):
		try:
			response = requests.get(self.apiJoin, timeout=self.timeout)
			if response.status_code == 200:
				content = response.text
				return json.loads(content)
		except Exception as e:
			raise Exception(f"Request {self.apiJoin} failed!\n{str(e)}")

		raise Exception(f"Request {self.apiJoin} returned invalid status({response.status_code})!")

	def _init(self, desc):
		self.vaultName = desc.get("name", "undefined")
		self.vaultEncoder = CreateEncoder(desc, False)

	def _info(self):
		try:
			response = requests.get(self.apiInfo, timeout=self.timeout)
			if response.status_code != 200:
				raise Exception(f"Request {self.apiInfo} failed with code {response.status_code}:\n{response.text}");
			content = response.text
			return json.loads(content)
		except Exception as e:
			raise Exception(f"Request {self.apiInfo} failed!\n{str(e)}")

	def ready(self):
		return self.vaultEncoder != None

	def info(self):
		result = self._info()
		result["connection"] = {
			"url" : self.url,
			"timeout" : self.timeout,
			"ready" : self.ready(),
		}
		return result

	def _execute(self, operation):

		operation.update(self.publicKey)

		if (self.vaultEncoder == None):
			raise Exception(f"Vault `{self.vaultName}` is not ready! -> {self.url}")

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

	def find(self, regex = ""):
		result = self._execute({
			"find" : regex
		})
		return result['find']

	def query(self, items_list):
		result = self._execute({
			"query" : items_list
		})
		return result['query']

	def update(self, dict_values):
		result = self._execute({
			"set" : dict_values
		})
		return result['set']

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






