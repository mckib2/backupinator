'''Target that clients send data to backed up at.'''

import pathlib
import logging

from backupinator import TargetDB
from backupinator.utils import (
    get_target_config_filename, get_generic_config_val)

class Target:
    '''Runs at remote site and gets client data from server.

    Notes
    -----

    Database:
        Client Table:
            clientID
            last_active

        Chunk Table:
            hash(plaintext)
            chunk_filename
            chunk_owner

        Filenames Table:
            filename_owner
            filename
            version
            timestamp
    '''

    def __init__(self, target_name):

        self.target_name = target_name

        # Set debug level
        log_format = "%(levelname)s:[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=log_format, level=logging.DEBUG)

        # Get where config file is
        self.configfile = get_target_config_filename(target_name)

        # get a database
        self.target_db = TargetDB(self.target_name)

        # Create the backup data directory if it doesn't exist
        self.backup_dir = self.get_config_val('backup_dir')
        pathlib.Path(self.backup_dir).mkdir(parents=True, exist_ok=True)

    def get_config_val(self, key, valtype='str'):
        '''Lookup value in target config file.'''
        return get_generic_config_val(self.configfile, key, valtype)

    def register_client(self, client_name):
        '''Setup a client for backup.'''

        # Add this client to the database
        self.target_db.add_client(client_name)

        # Make a directory for this client
        pathlib.Path(self.backup_dir / client_name).mkdir(
            parents=True, exist_ok=True)

    def update_file(self, client_name):
        '''Add or update a file stored on target.'''

        # Make sure client directory exists
