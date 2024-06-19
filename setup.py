from setuptools import setup, find_packages

directory = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(directory, 'secretsvault', '_version.py')).read())

setup(
    name = "pysecrets-vault",
    version = __version__,
    description = "The package handles a key value map with encoding for values. Siuted for secrets providers",
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    packages = find_packages(),
    install_requires = [
        "cryptography",
        "requests",
        "shared-memory-dict",
    ],
    python_requires = '>=3.6',
    entry_points = {
        'console_scripts': [
            'vault=vaultconsole.cli:main',
        ],
    }
)