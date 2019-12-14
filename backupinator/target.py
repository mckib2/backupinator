'''Target that clients send data to backed up at.'''

import pathlib
import logging

from backupinator import TargetDB
from backupinator.utils import (
    get_target_config_filename, get_generic_config_val)

class Target:
    '''Runs at remote site and gets client data from server.'''

    def __init__(self, target_name):

        self.target_name = target_name

        # Set debug level
        log_format = "%(levelname)s:[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=log_format, level=logging.DEBUG)

        # Get where config file is
        self.configfile = get_target_config_filename(target_name)

        # Create the backup data directory if it doesn't exist
        self.backup_dir = self.get_config_val('backup_dir')
        pathlib.Path(self.backup_dir).mkdir(parents=True, exist_ok=True)

        # get a database
        self.target_db = TargetDB(self.target_name, self.backup_dir)

    def get_config_val(self, key, valtype='str'):
        '''Lookup value in target config file.'''
        return get_generic_config_val(self.configfile, key, valtype)

    def get_client_directory(self, client_name):
        '''Return name of directory holding client data.'''
        return self.backup_dir / client_name

    def register_client(self, client_name):
        '''Setup a client for backup.'''

        # Add this client to the database
        self.target_db.add_client(client_name)

        # Make a directory for this client
        pathlib.Path(self.get_client_directory(client_name)).mkdir(
            parents=True, exist_ok=True)

    def update_file(self, client_name, filename_hash, data):
        '''Add or update a file stored on target.'''

        # Make sure client directory exists
        client_dir = self.get_client_directory(client_name)
        client_dir.mkdir(parents=True, exist_ok=True)

        # Add data to backup_dir
        with open(client_dir / filename_hash, 'wb') as f:
            f.write(data)

        # Add filename to database
        self.target_db.add_file(client_name, filename_hash)
