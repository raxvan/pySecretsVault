
import requests
import json
import os

from .vault_encoder import CreateEncoderWith
from .vault_encoder import CreateNewEncoder

_timeout = 2 #2 sec

def CreateVaultImpl(config):
	url = config.get('url', None)
	if url != None:
		return RemoteVault(url, config)


class ApiMap():
	def __init__(self, url):
		self.apiExec = f"{url}/exc"
		self.apiInfo = f"{url}/info"
		self.apiUnlock = f"{url}/unlock"
		self.url = url

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
				raise Exception(f"Failed to create vault encoder for {url}. No public key provided!")

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

	def _info(self):
		try:
			response = requests.get(self.apiInfo, timeout=self.timeout)
			if response.status_code != 200:
				raise Exception(f"Request {self.apiInfo} failed with code {response.status_code}:\n{response.text}");
			content = response.text
			return json.loads(content)
		except Exception as e:
			raise Exception(f"Request {self.apiInfo} failed!\n{str(e)}")

	def info(self):
		result = self._info()
		result["url"] = self.url
		result["timeout"] = self.timeout
		return result

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






