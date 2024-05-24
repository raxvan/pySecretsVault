from flask import Flask, request, jsonify, Response
import os
import re
import sys
import json
import secretsvault

VERSION = os.environ.get("VAULT_VERSION", "0.0.0")
HOST=os.environ.get("VAULT_HOST", "0.0.0.0")
PORT=int(os.environ.get("VAULT_PORT", "5000"))
MAX_REQUEST_SIZE = int(os.environ.get("VAULT_MAX_REQUEST_SIZE", str(1024 * 1024)))
CONFIG_FOLDER = os.environ.get("VAULT_CONFIG_DIR", '/vault/config')
DATA_FOLDER = os.environ.get("VAULT_DATA_DIR", '/vault/data')
VAULT_SERVER_MODE = os.environ.get("VAULT_SERVER_MODE", "")
VAULT_PUBLISH_KEY = os.environ.get("VAULT_PUBLISH_KEY", "FALSE").upper() == "TRUE"
################################################################################################################

CONFIG_STORAGE = secretsvault.CreateFileStorage(CONFIG_FOLDER, False)
DATA_STORAGE = secretsvault.CreateFileStorage(DATA_FOLDER, True)

ENCODER = secretsvault.CreateEncoder(CONFIG_STORAGE, False) #this can never be True
if ENCODER == None:
	raise Exception("Failed to create encoder!")

WHITELIST = CONFIG_STORAGE.get("whitelist", None)
if WHITELIST == None:
	WHITELIST = set()
else:
	WHITELIST = set(json.loads(WHITELIST))

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
	if secretsvault.InspectDataForKeys(CONFIG_STORAGE) != None:
		return "ERRPR: Systems locked!", 300

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

def _is_whitelisted(rq):
	if request.remote_addr in WHITELIST:
		return True
	return False

@app.route('/join', methods=['GET'])
def routeJoin():
	if VAULT_PUBLISH_KEY == True:
		return ENCODER.get_public_data(), 200
	
	lockedStatus = secretsvault.InspectDataForKeys(CONFIG_STORAGE)
	whitelisted =_is_whitelisted(request)
	if lockedStatus == None and whitelisted == True:
		return ENCODER.get_public_data(), 200

	return f"ERROR: System deflect!", 405

@app.route('/info', methods=['GET'])
def routeInfo():
	whitelisted = _is_whitelisted(request)

	info = {
		"version" : VERSION,
		"lockStatus" : secretsvault.InspectDataForKeys(CONFIG_STORAGE),
		"remote_addr" : request.remote_addr,
		"allowed" : whitelisted,
		"maxq" : MAX_REQUEST_SIZE,
		"mode" : VAULT_SERVER_MODE,
	}

	if VAULT_PUBLISH_KEY or whitelisted:
		info.update(ENCODER.get_public_data())
	return info, 200

@app.route('/unlock', methods=['GET'])
def routeUnlock():
	CONFIG_STORAGE.clear()
	return "OK", 200

################################################################################################################

if __name__ == '__main__':
	
	print(f">> Server mode [{VAULT_SERVER_MODE}] ")

	_debug = True if VAULT_SERVER_MODE == "debug" else False

	app.run(
		debug=_debug,
		host=HOST,
		port=PORT
	)
