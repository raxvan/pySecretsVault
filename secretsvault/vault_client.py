
import requests
import json

from .vault_encoder import CreateEncoderWith
from .vault_encoder import CreateNewEncoder

_timeout = 2 #2 sec

def CreateVaultImpl(desc):
	url = desc.get('url', None)
	if url != None:
		return RemoteVault(url, desc)


class ApiMap():
	def __init__(self, url):
		self.apiExec = f"{url}/exc"
		self.apiInfo = f"{url}/info"
		self.apiSanitize = f"{url}/sanitize"


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

	def sanitize(self):
		try:
			response = requests.get(self.apiSanitize, timeout=self.timeout)
			if response.status_code != 200:
				raise Exception(f"Request {self.apiSanitize} failed with code {response.status_code}!");
			
		except Exception as e:
			raise Exception(f"Request {self.apiSanitize} failed!\n{str(e)}")

		return True			

	def info(self):
		try:
			response = requests.get(self.apiInfo, timeout=self.timeout)
			if response.status_code != 200:
				raise Exception(f"Request {self.apiInfo} failed with code {response.status_code}!");
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
				raise Exception(f"Request {self.apiExec} failed with code {response.status_code}!");
			reply = self.upstreamEncoder.decodeStr(response.content)
			return json.loads(reply)
		except Exception as e:
			raise Exception(f"Request {self.apiExec} failed!\n{str(e)}")

	def keys(self, regex = ""):
		result = self._execute({
			"keys" : regex
		})
		return result['keys']


	def __getitem__(self, key):
		result = self._execute({
			"get" : [key]
		})
		return result['get'].get(key, None)

	def __setitem__(self, key, value):
		result = self._execute({
			"set" : {
				key : value
			}
		})
		return result['set'] == 1


	
		


	