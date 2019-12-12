'''Target that clients send data to backed up at.'''

import logging

class Target:

    def __init__(self):

        # Set debug level
        log_format = "%(levelname)s:[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=log_format, level=logging.DEBUG)
