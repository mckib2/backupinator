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
    #
    # # Coerce a type:
    # return {
    #     'str': ,
    #     'int': ,
    #     'float': config.getfloat('DEFAULT', key),
    #     'bool': config.getboolean('DEFAULT', key)
    # }[valtype]
