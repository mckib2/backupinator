'''Client to send jobs to server.'''

import pathlib
from time import time
import json

from Cryptodome.PublicKey import RSA # pylint: disable=E0401
from Cryptodome.Signature import pkcs1_15 # pylint: disable=E0401
from Cryptodome.Hash import SHA256 # pylint: disable=E0401

from backupinator import Job
from backupinator.utils import get_config_val, random_string

class Client:
    '''Produce jobs to send to server.'''

    def __init__(self):

        # Get client name from config
        self.client_name = get_config_val('client_name')

        # Job queues
        self.jobs = {} # for connected targets
        self.defered_jobs = {} # if we lose connection, keep backlog

        # Get targets
        self.targets = get_config_val('targets').split(',')

        # All targets should be synced from the start
        self.unsynced_targets = self.targets.copy()

        # Initialize job queues
        for target in self.targets:
            self.jobs[target] = []
            self.defered_jobs[target] = []

        # Set up a local backup if user wants it
        self.local_target = get_config_val('local_target')
        if self.local_target is not None:
            self.local_target = pathlib.Path(self.local_target)
            self.local_target.mkdir(parents=True, exist_ok=True)

        # Generate an RSA key pair if none exists
        dirpath = pathlib.Path(
            'client_data/%s/rsa_keys/' % self.client_name)
        rsa_pub_key_filename = (
            dirpath / 'backupinator_rsa_public_key.pem')
        rsa_priv_key_filename = (
            dirpath / 'backupinator_rsa_private_key.pem')
        infopath = pathlib.Path(dirpath / 'backupinator_rsa_info.txt')
        if not infopath.exists():

            # Write the private key
            key_size = 2048
            key = RSA.generate(key_size)
            private_key = key.export_key()
            rsa_priv_key_filename.parents[0].mkdir(parents=True, exist_ok=True)
            with open(str(rsa_priv_key_filename), 'wb') as file:
                file.write(private_key)

            # Write the public key
            public_key = key.publickey().export_key()
            rsa_pub_key_filename.parents[0].mkdir(
                parents=True, exist_ok=True)
            with open(str(rsa_pub_key_filename), 'wb') as file:
                file.write(public_key)

            # Write the info file
            infopath.parents[0].mkdir(parents=True, exist_ok=True)
            with open(str(infopath), 'w') as file:
                file.write(
                    'key_size=%d\ntimestamp=%d' % (key_size, time()))

        # Load RSA public key
        with open(str(rsa_pub_key_filename), 'rb') as file:
            self.rsa_pub_key = file.read()

        # Load RSA private key
        with open(str(rsa_priv_key_filename), 'rb') as file:
            self.rsa_priv_key = file.read()

        # Read signature length from the config file
        self.auto_signature_len = get_config_val(
            'auto_signature_len', valtype='int')

    def sign_with_priv_key(self, message=None):
        '''Sign message with private key.'''

        # Random message if not provided
        if message is None:
            message = random_string(self.auto_signature_len)

        hashed = SHA256.new(message.encode())
        key = RSA.import_key(self.rsa_priv_key)
        signature = pkcs1_15.new(key).sign(hashed)
        return(message, signature.hex())

    def register(self):
        '''Register with the server.'''

        # Create a registration job
        message, signature = self.sign_with_priv_key()
        job = Job({
            'job_type': 'register_client',
            'client_name': self.client_name,
            'rsa_pub_key': self.rsa_pub_key.decode(),
            'message': message,
            'signature': signature,
        })

        # Submit the job
        _resp = job.submit()

        print(_resp)

    def checkin(self):
        '''Tell the server that we are active.'''

        # Create a checkin job
        message, signature = self.sign_with_priv_key()
        job = Job({
            'job_type': 'checkin_client',
            'client_name': self.client_name,
            'target_list': self.targets,
            'message': message,
            'signature': signature,
        })

        # Submit the job
        resp = job.submit()
        json_data = json.loads(resp.text)

        # Defer jobs for targets who aren't online
        for target in json_data['offline_targets']:
            self.defered_jobs[target] += self.jobs[target].copy()
            self.jobs[target] = []

        # Add back jobs for any targets came back online
        for target in json_data['online_targets']:
            self.jobs[target] += self.defered_jobs[target].copy()
            self.defered_jobs[target] = []


    def sync_target(self, target_name):
        '''Ask server for target's tree so we know what to send.'''

        message, signature = self.sign_with_priv_key()
        job = Job({
            'job_type': 'get_tree',
            'client_name': self.client_name,
            'target_name': target_name,
            'message': message,
            'signature': signature,
        })

    def list_jobs(self):
        '''Print out a list of all jobs this client has.'''
        print('Jobs: ', json.dumps(self.jobs, indent=2))
        print('Defered: ', json.dumps(self.defered_jobs, indent=2))

    def dummy_jobs(self):
        '''Add dummy test jobs.'''

        # for


if __name__ == '__main__':

    client = Client()

    # Try registering
    client.register()

    # Try checking in
    client.checkin()

    # Checkout job queues
    client.list_jobs()
