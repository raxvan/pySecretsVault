
import os
import sys
import argparse
import json

import tempfile
import subprocess

import secretsvault

def _read_desc(basedir, name):
	try:
		f = open(os.path.join(basedir, name), "r")
		content = json.load(f)
		f.close()
		return content
	except:
		return None

def open_vault(basedir):
	return secretsvault.OpenVault()

def _do_set(basedir, key, value):

	vault = open_vault(basedir)
	if value == None:
		import getpass
		value = getpass.getpass("Value:")
	
	vault[key] = value

def _do_get(basedir, key, clean):
	vault = open_vault(basedir)

	value = vault[key]
	if value != None and clean:
		print(value, end="")
	elif value != None:
		print("-" * 128 + f"\n{value}\n" + "-" * 128)
	elif clean == False:
		print("\nNot found!\n")

def _do_list(basedir, regex):
	vault = open_vault(basedir)
	index = 0
	for k in vault.keys(regex if regex != None else ""):
		print(str(index).rjust(4) + f" | {k}")
		index += 1

def _do_find(basedir, regex):
	vault = open_vault(basedir)
	items = vault.find(regex)
	print(f"Items found:{len(items)}")

	for k, v in items.items():
		print(str(k).rjust(32) + f" | {v}")

def _locate_file(basedir, path):
	if os.path.exists(path):
		return os.path.abspath(path)

	if os.path.isabs(path):
		return path
	return os.path.abspath(os.path.join(basedir, path))


def _get_file_password(vault, filename):
	key = vault[filename]
	if key == None:
		import getpass
		key = getpass.getpass(f"[{filename}] TOKEN:")
		if key == "":
			import secrets
			import string
			characters = string.ascii_letters + string.digits + string.punctuation
			key = ''.join(secrets.choice(characters) for i in range(64))

		vault[filename] = key

	return key

def _do_edit(basedir, path):
	file = _locate_file(basedir, path)
	folder, filename = os.path.split(file)

	temp = tempfile.NamedTemporaryFile(delete=False)
	tfpath = temp.name
	temp.close()

	vault = open_vault(basedir)

	pwd = _get_file_password(vault, filename)

	if os.path.exists(file):
		secretsvault.vault_decode_file(pwd, file, tfpath)

	subprocess.run(['nano', tfpath])

	secretsvault.vault_encode_file(pwd, tfpath, file)

	os.remove(tfpath)

def _do_load(basedir, path):
	file = _locate_file(basedir, path)
	folder, filename = os.path.split(file)

	vault = open_vault(basedir)
	content = secretsvault.vault_decode_file(_get_file_password(vault, filename), file, None)
	try:
		content = json.loads(content)
	except:
		raise Exception(f"Failed to decode file {file}")

	vault.update(content)


def _do_cat(basedir, path):
	file = _locate_file(basedir, path)

	if not os.path.exists(file):
		raise Exception(f"Could not find {file}")

	folder, filename = os.path.split(file)

	vault = open_vault(basedir)
	content = secretsvault.vault_decode_file(_get_file_password(vault, filename), file, None)
	print(content)

def _do_info(basedir, url):
	vault = open_vault(basedir)
	inf = vault.info()
	content = json.dumps(inf, indent = 2)
	print(content)

def _do_unlock(basedir):
	vault = open_vault(basedir)
	vault.unlock()

def _do_main(args):
	basedir = os.getcwd()

	acc = args.action
	if acc == "set":
		_do_set(basedir, args.key, args.value)
	elif acc == "get":
		_do_get(basedir, args.key, args.clean)
	elif acc == "list":
		_do_list(basedir, args.regex)
	elif acc == "info":
		_do_info(basedir, args.url)
	elif acc == "edit":
		_do_edit(basedir, args.path)
	elif acc == "cat":
		_do_cat(basedir, args.path)
	elif acc == "load":
		_do_load(basedir, args.path)
	elif acc == "find":
		_do_find(basedir, args.regex)
	elif acc == "unlock":
		_do_unlock(basedir)
	os.chdir(basedir)

def main():
	user_arguments = sys.argv[1:]

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(description='Actions:')

	_set_parser = subparsers.add_parser('set', description='Update (or create) the value of a key using hidden input.')
	_set_parser.set_defaults(action='set')
	_set_parser.add_argument('key', help='The key must respect file naming conventions.')
	_set_parser.add_argument('value', nargs='?', default=None, help='The value can be anything')

	_edit_parser = subparsers.add_parser('edit', description='Edit a vault file.')
	_edit_parser.set_defaults(action='edit')
	_edit_parser.add_argument('path', help='File path to edit')

	_load_parser = subparsers.add_parser('load', description='Loads from an encoded file into the vault')
	_load_parser.set_defaults(action='load')
	_load_parser.add_argument('path', help='File encoded vault')

	_cat_parser = subparsers.add_parser('cat', description='Prints content of a vault file.')
	_cat_parser.set_defaults(action='cat')
	_cat_parser.add_argument('path', help='File path to edit')

	_get_parser = subparsers.add_parser('get', description='Prints the value of the key.')
	_get_parser.set_defaults(action='get')
	_get_parser.add_argument('-c', '--clean', dest='clean', action='store_true', help="Clean print, no extra spaces, newlinst, etc.")
	_get_parser.add_argument('key', help='The entry key')

	_list_parser = subparsers.add_parser('list', description='Lists entry keys.')
	_list_parser.set_defaults(action='list')
	_list_parser.add_argument('regex', nargs='?', default="", help='Optional key search regex')

	_find_parser = subparsers.add_parser('find', description='Finds entries with values.')
	_find_parser.set_defaults(action='find')
	_find_parser.add_argument('regex', help='Key search regex')

	_vault_info = subparsers.add_parser('info', description='Show vault information.')
	_vault_info.set_defaults(action='info')
	_vault_info.add_argument('url', nargs='?', default="", help='The vault url to query the info from')

	_vault_unlock = subparsers.add_parser('unlock', description='Unlock vault for usage.')
	_vault_unlock.set_defaults(action='unlock')
	
	
	args = parser.parse_args(user_arguments)

	if hasattr(args, 'action'):
		_do_main(args)
	else:
		print("Missing operation:")
		for k,_ in subparsers.choices.items():
			print(f"\t-> {k}")

