from setuptools import setup, find_packages

setup(
    name = "pysecrets-vault",
    version = "0.0.1",
    description = "The package handles a key value map with encoding for values. Siuted for secrets providers",
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    packages = find_packages(),
    install_requires = [
        "cryptography",
        "gunicorn",
        "flask",
        "requests"
    ],
    python_requires = '>=3.6',
    entry_points = {
        'console_scripts': [
            'vault=vaultconsole.cli:main',
        ],
    }
)