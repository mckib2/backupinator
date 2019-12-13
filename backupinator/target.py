'''Target that clients send data to backed up at.'''

import logging

class Target:
    '''Runs at remote site and gets client data from server.'''

    def __init__(self, target_name):

        self.target_name = target_name

        # Set debug level
        log_format = "%(levelname)s:[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=log_format, level=logging.DEBUG)

        # # Get target name from config
        # self.target_name = get_config_val('target_name')
