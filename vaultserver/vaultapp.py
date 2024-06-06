
import os
import re
import sys
import json
import secretsvault
import subprocess
import netifaces as ni

from flask import Flask, request, jsonify, Response
from shared_memory_dict import SharedMemoryDict
from ipaddress import ip_address, ip_network

MAX_REQUEST_SIZE = int(os.environ.get("VAULT_MAX_REQUEST_SIZE", str(1024 * 1024)))
DATA_FOLDER = os.environ.get("VAULT_DATA_DIR", '/vault/data')
NAME = os.environ.get("VAULT_NAME", 'vn')
MODE = os.environ.get("VAULT_SERVER_MODE", "")

VAULT_PUBLIC_ACCESS = os.environ.get("VAULT_PUBLIC_ACCESS", "")
################################################################################################################
def get_allowed_network(interface = "eth0"):
	if VAULT_PUBLIC_ACCESS != "subnet":
		return None
	addr = ni.ifaddresses(interface)[ni.AF_INET][0]
	ip_info = f"{addr['addr']}/{addr['netmask']}"
	network = ip_network(ip_info, strict=False)
	return network

################################################################################################################

DATA_STORAGE = secretsvault.CreateFileStorage(DATA_FOLDER, True)

CONFIG_STORAGE = SharedMemoryDict(name=f'{NAME}Config', size=2048)

STATUS = secretsvault.InspectDataForKeys(CONFIG_STORAGE)
ENCODER = secretsvault.CreateEncoder(CONFIG_STORAGE, False) #this can never be True

if ENCODER == None:
	raise Exception("Failed to create encoder!")

#CONFIG_STORAGE.shm.close()
#CONFIG_STORAGE.shm.unlink()

ALLOWED_NETWORK_SUBNET = get_allowed_network()

################################################################################################################

app = Flask(__name__)

################################################################################################################

def executeQuery(data):
	if not isinstance(data, list):
		raise Exception("<expected list with 'query'>")
	result = {}

	for k in data:
		ks = str(k)
		value = DATA_STORAGE[ks]
		if value == None:
			continue
		result[ks] = ENCODER.decodeStr(value)
	return result

def executeList(pattern):

	if pattern == "":
		return DATA_STORAGE.keys()
	
	try:
		compiled_pattern = re.compile(str(pattern))
	except:
		raise Exception(f"<invalid regex: {pattern}>")

	return [k for k in DATA_STORAGE.keys() if compiled_pattern.match(k)]
	
def executeFind(pattern):
	try:
		compiled_pattern = re.compile(str(pattern))
	except:
		raise Exception(f"<invalid regex: {pattern}>")

	return {k : ENCODER.decodeStr(DATA_STORAGE[k]) for k in DATA_STORAGE.keys() if compiled_pattern.match(k)}

def executeSet(data):
	if not isinstance(data, dict):
		raise Exception("<expected dict with 'set'>")

	index = 0
	
	for k,v in data.items():
		DATA_STORAGE[str(k)] = ENCODER.encodeStr(str(v))
		index += 1

	return index

def executePacket(packet):
	clientEncoder = secretsvault.CreateEncoder(packet, False)
	if clientEncoder == None:
		raise Exception("<missing client token>")

	out = {}
	
	_queryPacket = packet.get("query", None)
	if _queryPacket != None:
		out["query"] = executeQuery(_queryPacket)

	_setPacket = packet.get("set", None)
	if _setPacket != None:
		out["set"] = executeSet(_setPacket)

	_listPacket = packet.get("list", None)
	if _listPacket != None:
		out["list"] = executeList(_listPacket)

	_findPacket = packet.get("find", None)
	if _findPacket != None:
		out["find"] = executeFind(_findPacket)

	return clientEncoder.encodeStr(json.dumps(out))

################################################################################################################

@app.route('/exc', methods=['POST']) 
def routeExecute():
	content_length = request.headers.get('Content-Length')
	if content_length is None:
		return "ERROR: Invalid request!", 400
	
	try:
		content_length = int(content_length)
		if content_length > MAX_REQUEST_SIZE:
			raise
	except:
		print(f"Invalid Content-Length {content_length}", file=sys.stderr)
		return "ERROR: Systems overload!", 401

	try:
		packet = ENCODER.decodeStr(request.stream.read(content_length))
	except Exception as e:
		print(f"Decode error occurred: {e}", file=sys.stderr)
		return "ERROR: Systems corrupted!", 402

	try:
		packet = json.loads(packet)
	except Exception as e:
		print(f"Json Parse error occurred: {e}", file=sys.stderr)
		return "ERROR: Systems miscommunication!", 403

	try:
		return Response(executePacket(packet), mimetype='application/octet-stream')
	except Exception as e:
		print(f"Execute error: {e}", file=sys.stderr)
		return f"ERROR: Systems wispered error!", 404

def _allow_access(rq):
	if VAULT_PUBLIC_ACCESS == "enable":
		return True
	if ALLOWED_NETWORK_SUBNET == None:
		return False
	if ip_address(rq.remote_addr) in ALLOWED_NETWORK_SUBNET:
		return True
	return False

@app.route('/join', methods=['GET'])
def routeJoin():
	if _allow_access(request) == True:
		k,v = ENCODER.get_public_key()

		return {
			"name" : NAME,
			k : v,
		}, 200

	return f"ERROR: System disconnected!", 405

@app.route('/info', methods=['GET'])
def routeInfo():
	allowed = _allow_access(request)
	
	info = {
		"state" : STATUS,
		"remote_addr" : request.remote_addr,
		"allowed" : allowed,
		"maxq" : MAX_REQUEST_SIZE,
		"mode" : MODE,
		"access" : VAULT_PUBLIC_ACCESS,
		"name" : NAME,
		"server" : secretsvault.details(),
	}

	return info, 200

################################################################################################################

if __name__ == '__main__':
	
	HOST=os.environ.get("VAULT_HOST", "0.0.0.0")
	PORT=int(os.environ.get("VAULT_PORT", "5000"))

	print(f">> Server mode [{MODE}] ")

	_debug = True if MODE == "debug" else False

	app.run(
		debug=_debug,
		host=HOST,
		port=PORT
	)
