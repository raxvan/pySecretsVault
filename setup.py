from setuptools import setup, find_packages

setup(
    name="pysecrets-vault",
    version="0.0.1",
    description="The package handles a key value map with encoding for values. Siuted for secrets providers",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # If you have a README.md file
    packages=find_packages(),
    install_requires=[
        "cryptography"
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
)