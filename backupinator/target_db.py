'''Abstraction for SQL database for the target.'''

import sqlite3
import contextlib
import pathlib

class TargetDB:
    '''Database methods for the target.'''

    def __init__(self, target_name, backup_dir):

        self.target_name = target_name
        self.database_filename = pathlib.Path(backup_dir) / 'target.db'

    def create_db(self):
        '''Create database and tables.'''

        conn_string = 'file:%s?mode=rwc' % self.database_filename
        with contextlib.closing(sqlite3.connect(conn_string)) as con:

            # Create each of the tables if they don't exist
            sql_clients = '''CREATE TABLE IF NOT EXISTS clients (
                client_name text PRIMARY KEY
            );'''

            sql_filenames = '''CREATE TABLE IF NOT EXISTS filenames (
                filename text PRIMARY KEY,
                path_to_filename text NOT NULL,
                client_name NOT NULL,
                last_updated text NOT NULL,
                FOREIGN KEY (client_name) REFERENCES clients (client_name)
            );'''

            with con as cur:
                cur.execute(sql_clients)
                cur.execute(sql_filenames)

    def add_client(self, client_name):
        '''Add client.'''

        conn_string = 'file:%s?mode=w' % self.database_filename
        with contextlib.closing(sqlite3.connect(conn_string)) as con:

            sql = '''INSERT INTO clients (client_name)
                VALUES (%s);''' % client_name

            with con as cur:
                cur.execute(sql)


    def add_file(self):
        '''Add a backedup file.'''
