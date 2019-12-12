'''Utility functions.'''

from random import choice
import string
import configparser

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
