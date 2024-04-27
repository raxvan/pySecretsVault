from flask import Flask, request, jsonify, Response
import os
import re
import json
import secretsvault

VERSION = "0.0.1"
FILE_FOLDER = '/vault'
MAX_REQUEST_SIZE = 1024 * 1024
HOST="0.0.0.0"
PORT=5000
SERVER_MODE = os.environ.get("SERVER_MODE", "")

################################################################################################################

app = Flask(__name__)

################################################################################################################

CONFIG_STORAGE = secretsvault.CreateFileStorage(os.path.join(FILE_FOLDER,"config"), False)
DATA_STORAGE = secretsvault.CreateFileStorage(os.path.join(FILE_FOLDER,"data"), True)

ENCODER = secretsvault.CreateEncoder(CONFIG_STORAGE, True)
ENCODER.serialize(CONFIG_STORAGE)

################################################################################################################

def executeGet(data):
	result = {}
	for k in data:
		value = DATA_STORAGE[k]
		if value == None:
			continue
		result[k] = ENCODER.decodeStr(value)
	return result

def executeKeys(data):
	if data == "":
		return DATA_STORAGE.keys()
	
	compiled_pattern = re.compile(pattern)

	return [k for k in DATA_STORAGE.keys() if compiled_pattern.match(k)]
	

def executeSet(data):
	index = 0
	for k,v in data.items():
		DATA_STORAGE[k] = ENCODER.encodeStr(v)
		index += 1

	return index

def executePacket(packet):
	clientEncoder = secretsvault.CreateEncoder(packet, False)
	if clientEncoder == None:
		raise Exception("<missing client key>")

	out = {}
	
	_get = packet.get("get", None)
	if _get != None:
		out["get"] = executeGet(_get)

	_set = packet.get("set", None)
	if _set != None:
		out["set"] = executeSet(_set)

	_keys = packet.get("keys", None)
	if _keys != None:
		out["keys"] = executeKeys(_keys)

	return clientEncoder.encodeStr(json.dumps(out))

################################################################################################################

@app.route('/exc', methods=['POST'])
def routeExecute():
	if secretsvault.InspectDataForKeys(CONFIG_STORAGE) != None:
		return "ERROR: System not ready!", 300

	content_length = request.headers.get('Content-Length')
	if content_length is None:
		return "ERROR: Invalid request!", 400
	
	try:
		content_length = int(content_length)
		if content_length > MAX_REQUEST_SIZE:
			raise
	except:
		return "ERROR: Systems overload!", 401

	try:
		operation = ENCODER.decodeStr(request.stream.read(content_length))
	except:
		return "ERROR: Systems corrupted!", 402

	try:
		operation = json.loads(operation)
	except:
		return "ERROR: Systems miscommunication!", 403

	try:
		result = executePacket(operation)
		return Response(result, mimetype='application/octet-stream')
	except Exception as e:
		return f"ERROR: Systems wispered {str(e)}!", 404

@app.route('/info', methods=['GET'])
def routeInfo():
	info = {
		"version" : VERSION,
		"dirty" : secretsvault.InspectDataForKeys(CONFIG_STORAGE)
	}
	#info.update(ENCODER.get_public_data())
	return info, 200

@app.route('/sanitize', methods=['GET'])
def routeSanitize():
	CONFIG_STORAGE.clear()
	return "OK", 200

################################################################################################################

if __name__ == '__main__':
	
	print(f">>> Server mode [{SERVER_MODE}] ")

	_debug = True if SERVER_MODE == "debug" else False
	app.run(
		debug=_debug,
		host=HOST,
		port=PORT
	)
