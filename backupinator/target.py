'''Target that clients send data to backed up at.'''

import logging

from backupinator import TargetDB

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

        # # Get target name from config
        # self.target_name = get_config_val('target_name')

        # get a database
        self.target_db = TargetDB(self.target_name)
