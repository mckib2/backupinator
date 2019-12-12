'''Utility functions.'''

from random import choice
import string
import configparser
import pathlib
from time import time
import hashlib
import logging

from Cryptodome.PublicKey import RSA # pylint: disable=E0401

def random_string(nchar=10):
    '''Generate a random string of fixed length.'''
    return ''.join(choice(string.ascii_letters) for i in range(nchar))

def get_config_val(key, valtype='str'):
    '''Read value from config file.'''

    config = configparser.ConfigParser()
    config.read('config.ini')

    if valtype == 'str':
        return config['DEFAULT'][key]
    if valtype == 'int':
        return config.getint('DEFAULT', key)
    if valtype == 'float':
        return config.getfloat('DEFAULT', key)
    if valtype == 'bool':
        return config.getboolean('DEFAULT', key)

    raise ValueError('valtype not supported!')

def make_rsa_keys(public_filename, private_filename, key_size=2048):
    '''Make public and private keys if they don't exist.'''

    # filenames should be pathlib.Path objects
    assert isinstance(public_filename, pathlib.Path)
    assert isinstance(private_filename, pathlib.Path)

    # Generate an RSA key pair if none exists
    if not public_filename.exists() and not private_filename.exists():

        # Make the private key
        key = RSA.generate(key_size)
        private_key = key.export_key()

        # Make sure directories exist:
        private_filename.parents[0].mkdir(parents=True, exist_ok=True)

        # Write the key:
        with open(str(private_filename), 'wb') as file:
            file.write(private_key)

        # Make the public key
        public_key = key.publickey().export_key()

        # Make sure directories exist:
        public_filename.parents[0].mkdir(parents=True, exist_ok=True)

        # Write it to file:
        with open(str(public_filename), 'wb') as file:
            file.write(public_key)

    elif public_filename.exists() and private_filename.exists():
        pass # both keys exist -- good!
    else:
        raise ValueError('RSA key pair is missing or broken!')

def client_rsa_key_filename(client_name, public=True):
    '''Get the path of the public or private RSA key for client.'''

    dirpath = pathlib.Path(
        'client_data/%s/rsa_keys/' % client_name)

    if public:
        return dirpath / 'backupinator_rsa_public_key.pem'
    return dirpath / 'backupinator_rsa_private_key.pem'

def load_client_rsa_key(client_name, public=True):
    '''Get public or private RSA key from file.'''

    # Choose the correct filename
    filename = client_rsa_key_filename(client_name, public)

    # Load RSA key
    with open(str(filename), 'rb') as file:
        key = file.read()

    return key.decode()

def make_tree(hash_filenames=True, hash_times=True):
    '''Create hashes of filenames.'''

    # Get tracked files from config
    tracked_dirs = get_config_val('tracked_dirs').split(',')

    tree = {}
    t0 = time()
    for d in tracked_dirs:
        for file in pathlib.Path(d).rglob('*'):
            if file.is_file():

                key = str(file)
                if hash_filenames:
                    key = hashlib.sha224(key.encode()).hexdigest()

                val = str(file.stat().st_mtime)
                if hash_times:
                    val = hashlib.sha224(val.encode()).hexdigest()

                # Update file tree (list really...)
                tree[key] = val
    # print(tree)
    logging.info('Took %g sec to find all files', (time() - t0))

    return tree
