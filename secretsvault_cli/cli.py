
import os
import sys
import argparse

import secretsvault


def _do_register(basedir, key, value):
	storage = secretsvault.CreateFileStorage(basedir)
	enc = secretsvault.CreateEncoder(storage)
	enc.initialize()
	vault = secretsvault.CreateVault(enc, storage)

	vault.open(True)
	vault.setEnc(key, value)
	vault.close()

def _do_set(basedir, key):
	import getpass

	storage = secretsvault.CreateFileStorage(basedir)
	enc = secretsvault.CreateEncoder(storage)
	enc.initialize()

	vault = secretsvault.CreateVault(enc, storage)

	value = getpass.getpass("value:")
	vault.open(True)
	vault.set(key, value)
	encv = vault.getEnc(key)
	vault.close()

	print(f"vault register {key} {encv}")

def _do_show(basedir, key):
	storage = secretsvault.CreateFileStorage(basedir)
	enc = secretsvault.CreateEncoder(storage)
	enc.initialize()

	vault = secretsvault.CreateVault(enc, storage)

	vault.open(True)
	value = vault.get(key)
	vault.close()

	print(value)


def _do_main(args):
	basedir = os.getcwd()

	acc = args.action
	if acc == "register":
		_do_register(basedir, args.key, args.value)
	elif acc == "set":
		_do_set(basedir, args.key)
	elif acc == "show":
		_do_show(basedir, args.key)

	os.chdir(basedir)

def main():
	user_arguments = sys.argv[1:]

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(description='Actions:')

	_register_parser = subparsers.add_parser('register', description='Inserts into the vault an encrypted value.')
	_register_parser.set_defaults(action='register')
	_register_parser.add_argument('key', default=None, help='The entry name')
	_register_parser.add_argument('value', default=None, help='The entry value(encoded)')

	_set_parser = subparsers.add_parser('set', description='Inserts into the vault a value, printing the register command to add it.')
	_set_parser.set_defaults(action='set')
	_set_parser.add_argument('key', default=None, help='The entry name')

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

