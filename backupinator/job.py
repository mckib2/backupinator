'''Encapuslation of a job.'''

import requests
import jsons

from backupinator.utils import get_config_val

class Job:
    '''A task to be done by client or target.'''

    def __init__(self):
        pass

    def submit(self):
        '''Send the job to the server and return response.'''

        # Get server location from config file
        server_address = get_config_val('server_address')

        # Send a POST with this job
        self.job_type = self.__class__.__name__
        return requests.post(server_address, json=jsons.dump(self))

class RegisterClientJob(Job):
    '''Register a client'''

    def __init__(self, client_name, rsa_pub_key, auth):

        self.client_name = client_name
        self.rsa_pub_key = rsa_pub_key
        self.auth = auth

        # Call parent's init
        super(RegisterClientJob, self).__init__()

class CheckinClientJob(Job):
    '''Check client in.'''

    def __init__(self, client_name, target_list, auth):

        self.client_name = client_name
        self.target_list = target_list
        self.auth = auth

        # Call parent's init
        super(CheckinClientJob, self).__init__()

class GetTreeJob(Job):
    '''Get the target's tree to send to client.'''

    def __init__(self, client_name, target_name, auth):

        self.client_name = client_name
        self.target_name = target_name
        self.auth = auth

        # Call parent's init
        super(GetTreeJob, self).__init__()
