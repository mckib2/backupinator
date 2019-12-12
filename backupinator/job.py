'''Encapuslation of a job.'''

import requests

from backupinator.utils import get_config_val

class Job:
    '''A task to be done by client or target.'''

    TYPES = [
        'register_client',
        'checkin_client',
        'send_chunk',
        'get_tree',
    ]

    def __init__(self, data):

        self.job_type = data['job_type']
        assert self.job_type in self.TYPES, 'Not a valid job type!'

        # Bundle data with the Job
        self.data = data

        # Every job should have a message and signature
        assert 'message' in self.data
        assert 'signature' in self.data

        # Make sure members exist!
        {
            'register_client': self.check_register_client,
            'checkin_client': self.check_checkin_client,
            'get_tree': self.check_get_tree,
        }[self.job_type]()

        # Get server location from config file
        self.server_address = get_config_val('server_address')

    def check_register_client(self):
        '''Sanity check for client registration.'''
        assert 'client_name' in self.data
        assert 'rsa_pub_key' in self.data

    def check_checkin_client(self):
        '''Sanity check for client checkin.'''
        assert 'client_name' in self.data
        assert 'target_list' in self.data

    def check_get_tree(self):
        '''Sanity check for get target's tree.'''
        assert 'client_name' in self.data
        assert 'target_name' in self.data

    def submit(self):
        '''Send the job to the server and return response.'''
        return requests.post(self.server_address, json=self.data)
