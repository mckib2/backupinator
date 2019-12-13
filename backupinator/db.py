'''Abstraction to work with databases.'''

import dbm
import pathlib

class DB:
    '''Wrapper for simple key/val database.'''

    def __init__(self, name, dirname='db'):

        filepath = pathlib.Path(dirname) / name
        filepath.mkdir(parents=True, exist_ok=True)
        self.filename = str(filepath)

    def add(self, key, val):
        '''Add entry to database.'''

        with dbm.open(self.filename, 'c') as db:
            db[key] = val

    def get(self, key):
        '''Look up an entry in the database.'''

        with dbm.open(self.filename, 'r') as db:
            return db[key]

# import pathlib

# # Load CFFI variant
# # import os
# # os.environ['LMDB_FORCE_CFFI'] = '1'
# import lmdb # pylint: disable=E0401,C0413
#
# class DB:
#     '''Wrapper for database.'''
#
#     def __init__(self, name, dirname='db'):
#
#         # The actual database stuffs:
#         dirpath = pathlib.Path(dirname) / name
#         dirpath.mkdir(parents=True, exist_ok=True)
#         self._env = lmdb.Environment(
#             path=str(dirpath),
#             map_size=10485760,
#             subdir=True,
#             readonly=False,
#             metasync=True,
#             sync=True,
#             map_async=False,
#             mode=493,
#             create=True,
#             readahead=True,
#             writemap=False,
#             meminit=True,
#             max_readers=126,
#             max_dbs=0,
#             max_spare_txns=1,
#             lock=True)
#
#
#     def add(self, key, val):
#         '''Add an entry to the database.'''
#
#         with self._env.begin(write=True) as txn:
#             txn.put(key.encode(), val.encode(), dupdata=False)
#
#
#     def get(self, key):
#         '''Look up an entry in the database.'''
#
#         with self._env.begin(write=False) as txn:
#             return txn.get(key.encode(), default=None)
