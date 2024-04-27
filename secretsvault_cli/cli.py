
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
	directory = secretsvault.GetVaultDirectory(basedir)
	desc = _read_desc(directory, "main.json")
	if desc == None:
		raise Exception("Could not identify vault!")

	vault = secretsvault.CreateVault(desc)
	if vault == None:
		raise Exception("Could not load vault!")
	return vault

def _do_set(basedir, key, value):
	vault = open_vault(basedir)

	vault.setEnc(key, value)

def _do_create(basedir, key):
	import getpass

	vault = open_vault(basedir)

	value = getpass.getpass("value:")
	
	vault.set(key, value)
	encv = vault.getEncoded(key)

	print(f"vault set {key} {encv}")

def _do_show(basedir, key):
	vault = open_vault(basedir)

	value = vault.get(key)

	print("-" * 128 + f"\n{value}\n" + "-" * 128)

def _do_list(basedir):
	vault = open_vault(basedir)
	index = 0
	for k in vault.6():
		print(str(index).rjust(4) + f" | {k}")
		index += 1

def _do_info(basedir):
	vault = open_vault(basedir)

	print(f"Storage: {vault.getStorage().get_location()}")

def _do_main(args):
	basedir = os.getcwd()

	acc = args.action
	if acc == "set":
		_do_set(basedir, args.key, args.value)
	elif acc == "create":
		_do_create(basedir, args.key)
	elif acc == "show":
		_do_show(basedir, args.key)
	elif acc == "list":
		_do_list(basedir)
	elif acc == "info":
		_do_info(basedir)

	os.chdir(basedir)

def main():
	user_arguments = sys.argv[1:]

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(description='Actions:')

	_set_parser = subparsers.add_parser('set', description='Inserts into the vault an encrypted value.')
	_set_parser.set_defaults(action='set')
	_set_parser.add_argument('key', default=None, help='The entry key')
	_set_parser.add_argument('value', default=None, help='The entry value(encoded)')

	_create_parser = subparsers.add_parser('create', description='Create a new key/value pair from user input, printing the set command to add it.')
	_create_parser.set_defaults(action='create')
	_create_parser.add_argument('key', default=None, help='The entry key')

	_list_parser = subparsers.add_parser('list', description='Show all entries')
	_list_parser.set_defaults(action='list')

	_vault_info = subparsers.add_parser('info', description='Show vault information')
	_vault_info.set_defaults(action='info')

	_show_parser = subparsers.add_parser('show', description='Shows the decrypted value')
	_show_parser.set_defaults(action='show')
	_show_parser.add_argument('key', default=None, help='The entry name')
	
	args = parser.parse_args(user_arguments)

	if hasattr(args, 'action'):
		_do_main(args)
	else:
		print("Missing operation:")
		for k,_ in subparsers.choices.items():
			print(f"\t-> {k}")

