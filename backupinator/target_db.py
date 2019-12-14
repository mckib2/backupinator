'''Abstraction for database for the target.'''

import dbm
import contextlib
import pathlib
from time import time

class TargetDB:
    '''Database methods for the target.'''

    def __init__(self, target_name, backup_dir):

        self.target_name = target_name

        # Client DB
        self.backup_dir = pathlib.Path(backup_dir)
        self.client_db_filename = self.backup_dir / 'target_clients'
        pathlib.Path(self.client_db_filename).parents[0].mkdir(
            parents=True, exist_ok=True)

    def get_client_filenames_db_filename(self, client_name):
        '''Find where database is for storing filenames.'''
        return self.backup_dir / client_name / 'filenames'

    def add_client(self, client_name):
        '''Add client.'''

        with dbm.open(self.client_db_filename, 'c') as db:
            db[client_name] = True

        # Create a filenames database for this client
        filename = self.get_client_filenames_db_filename(client_name)
        pathlib.Path(filename).parents[0].mkdir(parents=True, exist_ok=True)

    def add_file(self, client_name, filename_hash):
        '''Add a backed-up file.'''

        db_filename = self.get_client_filenames_db_filename(client_name)
        with dbm.open(db_filename, 'c') as db:
            # Store with most recent time updated
            db[filename_hash] = str(time())
