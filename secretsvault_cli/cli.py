
import os
import sys
import argparse
import json

import secretsvault

def _read_desc(basedir, name):
	try:
		f = open(os.path.join(basedir, name), "r")
		content = json.load(f)
		f.close()
		return content
	except:
		return None

def open_vault(basedir, vaultdir):
	directory = secretsvault.FindVaultConfigFolder(basedir)
	desc = _read_desc(directory, "main.json")
	if desc == None:
		raise Exception(f"Could not identify vault in {directory}")

	vault = secretsvault.CreateVault(desc)
	if vault == None:
		raise Exception("Could not load vault!")
	return vault

def _do_set(basedir, key):
	import getpass

	vault = open_vault(basedir)
	value = getpass.getpass("Value:")
	
	vault[key] = value

def _do_get(basedir, key):
	vault = open_vault(basedir)

	value = vault.get(key, None)

	print("-" * 128 + f"\n{value}\n" + "-" * 128)

def _do_list(basedir):
	vault = open_vault(basedir)
	index = 0
	for k in vault.keys():
		print(str(index).rjust(4) + f" | {k}")
		index += 1

def _do_info(basedir):
	searchDir = secretsvault.FindVaultConfigFolder(basedir)
	print(f"Vault configs: {searchDir}")
	#vault = open_vault(basedir)

def _do_main(args):
	basedir = os.getcwd()

	acc = args.action
	if acc == "set":
		_do_set(basedir, args.key)
	elif acc == "get":
		_do_get(basedir, args.key)
	elif acc == "list":
		_do_list(basedir)
	elif acc == "info":
		_do_info(basedir)

	os.chdir(basedir)

def main():
	user_arguments = sys.argv[1:]

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(description='Actions:')

	_set_parser = subparsers.add_parser('set', description='Update (or create) the value of a key using hidden input.')
	_set_parser.set_defaults(action='set')
	_set_parser.add_argument('key', default=None, help='The entry key')

	_get_parser = subparsers.add_parser('get', description='Prints the value of the key.')
	_get_parser.set_defaults(action='get')
	_get_parser.add_argument('key', default=None, help='The entry key')

	_list_parser = subparsers.add_parser('list', description='Show all entries')
	_list_parser.set_defaults(action='list')

	_vault_info = subparsers.add_parser('info', description='Show vault information')
	_vault_info.set_defaults(action='info')

	
	
	args = parser.parse_args(user_arguments)

	if hasattr(args, 'action'):
		_do_main(args)
	else:
		print("Missing operation:")
		for k,_ in subparsers.choices.items():
			print(f"\t-> {k}")

