'''Key-value database for use with Client.'''

import dbm

from backupinator.utils import make_tree

class ClientDB:
    '''For simple file tracking for client.'''

    def __init__(self, client_name, get_config_val):
        self.client_name = client_name
        self.filename = 'client_data/%s/tree.db' % self.client_name

        # use client config function
        self.get_config_val = get_config_val

    def sync(self):
        '''Sync the database with the file system.'''

        hash_filenames = self.get_config_val('hash_filenames', valtype='bool')
        hash_times = self.get_config_val('hash_times', valtype='bool')
        tree = make_tree(self.client_name, hash_filenames, hash_times)

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
