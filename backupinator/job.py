'''Encapuslation of a job.'''

import uuid
import requests
import jsons # pylint: disable=E0401

__all__ = ['Job', 'BatchJob', 'RegisterClientJob', 'CheckinClientJob', 'GetTreeJob']

class Job:
    '''A task to be done by client or target.'''

    def __init__(self, server_address):

        # Save server_address so we know where to submit job
        self.server_address = server_address

        # Every job needs to know what kind of job it is for
        # deserialization:
        self.job_type = self.__class__.__name__

        # Give the job a unique id (uuid4 should be good enough
        # for our purposes)
        self.uuid = uuid.uuid4()

    def submit(self):
        '''Send the job to the server and return response.'''

        # Send a POST with this job
        return requests.post(self.server_address, json=jsons.dump(self))

class BatchJob(Job):
    '''A group of job objects to be sent to the server all at once.'''

    def __init__(self, server_address):
        self.jobs = []

        # Call parent's init
        super(BatchJob, self).__init__(server_address)

    def addjob(self, job):
        '''Add a job to the batch.'''
        self.jobs.append(job)

class RegisterClientJob(Job):
    '''Register a client'''

    def __init__(self, server_address, client_name, rsa_pub_key, auth):

        self.client_name = client_name
        self.rsa_pub_key = rsa_pub_key
        self.auth = auth

        # Call parent's init
        super(RegisterClientJob, self).__init__(server_address)

class CheckinClientJob(Job):
    '''Check client in.'''

    def __init__(self, server_address, client_name, target_list, auth):

        self.client_name = client_name
        self.target_list = target_list
        self.auth = auth

        # Call parent's init
        super(CheckinClientJob, self).__init__(server_address)

class GetTreeJob(Job):
    '''Get the target's tree to send to client.'''

    def __init__(self, server_address, client_name, target_name, auth):

        self.client_name = client_name
        self.target_name = target_name
        self.auth = auth

        # Call parent's init
        super(GetTreeJob, self).__init__(server_address)
