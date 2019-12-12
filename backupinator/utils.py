'''Utility functions.'''

from random import choice
import string
import configparser
import pathlib

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
