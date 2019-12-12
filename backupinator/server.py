'''Server handles passing of jobs between clients and targets.'''

from time import time

from Cryptodome.PublicKey import RSA # pylint: disable=E0401
from Cryptodome.Signature import pkcs1_15 # pylint: disable=E0401
from Cryptodome.Hash import SHA256 # pylint: disable=E0401

from backupinator import DB, Job, RegisterClientJob, CheckinClientJob, GetTreeJob

class Server:
    '''Coordinating server to handle jobs.'''

    def __init__(self, client_db_name='client_db'):

        self.client_db = DB(client_db_name)

        self.clients = {}
        self.targets = {}

    def authenticate_client(
            self, client_name, auth, rsa_pub_key=None):
        '''Make sure client's signature is correct.'''

        if rsa_pub_key is None:
            rsa_pub_key = self.client_db.get(client_name)

        # auth ends up as a dictionary after deserialization...
        hashed = SHA256.new(auth['message'].encode())
        key = RSA.import_key(rsa_pub_key)
        try:
            pkcs1_15.new(key).verify(
                hashed, bytes.fromhex(auth['hex_signature']))
            return True
        except (ValueError, TypeError):
            return False

    def job_handler(self, job):
        '''Given a job, decide what to do about it.'''

        # Sanity check
        assert isinstance(job, Job), 'Must use a Job object!'

        # Do the right thing based on job type
        return {
            RegisterClientJob: self.register_client,
            CheckinClientJob: self.checkin_client,
            GetTreeJob: self.get_tree,
        }[type(job)](job)

    def register_client(self, job):
        '''Add a client to the database.'''

        # Authenticate
        if self.authenticate_client(
                job.client_name, job.auth, job.rsa_pub_key):
            self.client_db.add(job.client_name, job.rsa_pub_key)
            return {
                'success': True
            }

        return {
            'success': False,
            'msg': 'Could not authenticate client!'
        }


    def checkin_client(self, job):
        '''Mark a client as active.'''

        # Authenticate client
        if not self.authenticate_client(job.client_name, job.auth):
            return {
                'success': False,
                'msg': 'Could not authenticate client!'
            }

        # Only point to targets that are online.
        offline_targets = [t for t in job.target_list if t not in self.targets]
        online_targets = [t for t in job.target_list if t in self.targets]
        self.clients[job.client_name] = {
            'last_checkin': time(),
            'target_list': online_targets,
        }

        # Tell client which targets are online, offline
        return {
            'success': True,
            'online_targets': online_targets,
            'offline_targets': offline_targets,
        }


    def get_tree(self, job):
        '''Get the directory tree as recorded on the target.'''

        # Authenticate client
        if not self.authenticate_client(job.client_name, job.auth):
            return {
                'success': False,
                'msg': 'Could not authenticate client!'
            }

        # We can't do anything if the target is offline
        if job.target_name not in self.targets:
            return {
                'success': False,
                'msg': 'target is offline -- job cannot be queued.'
            }

        raise NotImplementedError()

        # # We can make job for the target
        # self.targets[job.target_name]['jobs'][job.client_name].append(Job({
        #     'job_type': 'send_tree',
        #     'target_name': target_name,
        #     'client_name': client_name,
        # }))
        #
        # return {
        #     'success': True,
        #     'msg': '"get_tree" job queued.'
        # }
