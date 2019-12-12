'''Key-value database for use with Client.'''

import dbm
import pathlib

from backupinator.utils import get_config_val, make_tree

class ClientDB:
    '''For simple file tracking for client.'''

    def __init__(self, client_name):
        self.filename = 'client_data/%s/tree.db' % client_name

    def sync(self):
        '''Sync the database with the file system.'''

        hash_filenames = get_config_val('hash_filenames', valtype='bool')
        hash_times = get_config_val('hash_times', valtype='bool')
        tree = make_tree(hash_filenames, hash_times)

        # Easiest way to sync is to recreate database:
        with dbm.open(self.filename, 'n') as db:
            for key, val in tree.items():
                db[key] = val


    def update(self, key, val):
        '''Update an entry in the database.'''

        with dbm.open(self.filename, 'c') as db:
            db[key] = val

    def remove(self, key):
        '''Remove an entry from database.'''

        with dbm.open(self.filename, 'c') as db:
            try:
                del db[key]
            except KeyError:
                pass
