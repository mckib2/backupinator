'''Client to send jobs to server.'''

import pathlib
import json
import logging

from Cryptodome.PublicKey import RSA # pylint: disable=E0401
from Cryptodome.Signature import pkcs1_15 # pylint: disable=E0401
from Cryptodome.Hash import SHA256 # pylint: disable=E0401

from backupinator import Auth, ClientDB
from backupinator.job import *
from backupinator.utils import (
    get_generic_config_val, random_string, make_rsa_keys,
    client_rsa_key_filename, load_client_rsa_key,
    get_client_config_filename)

class Client:
    '''Produce jobs to send to server.'''

    def __init__(self, client_name):

        # Set debug level
        log_format = "%(levelname)s:[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=log_format, level=logging.DEBUG)

        # Get associated config file
        self.client_name = client_name
        self.configfile = get_client_config_filename(self.client_name)

        # Get server address from config file
        self.server_address = self.get_config_val('server_address')

        # Job queues
        self.jobs = {} # for connected targets
        self.defered_jobs = {} # if we lose connection, keep backlog

        # Get targets
        self.targets = self.get_config_val('targets').split(',')

        # All targets should be synced from the start
        self.unsynced_targets = self.targets.copy()

        # Initialize job queues
        for target in self.targets:
            self.jobs[target] = []
            self.defered_jobs[target] = []

        # Set up a local backup if user wants it
        self.local_target = self.get_config_val('local_target')
        if self.local_target is not None:
            self.local_target = pathlib.Path(self.local_target)
            self.local_target.mkdir(parents=True, exist_ok=True)

        # Generate an RSA key pair if none exists
        public_filename = client_rsa_key_filename(
            self.client_name, public=True)
        private_filename = client_rsa_key_filename(
            self.client_name, public=False)
        make_rsa_keys(
            public_filename, private_filename, key_size=2048)

        # Read signature length from the config file
        self.auto_signature_len = self.get_config_val(
            'auto_signature_len', valtype='int')

        # Sync up the database with the filesystem
        self.client_db = ClientDB(
            self.client_name, self.get_config_val)
        self.client_db.sync()

    def get_config_val(self, key, valtype='str'):
        '''Lookup value in client config file.'''
        return get_generic_config_val(self.configfile, key, valtype)

    def sign_with_priv_key(self, message=None):
        '''Sign message with private key.'''

        # Random message if not provided
        if message is None:
            message = random_string(self.auto_signature_len)

        # Load the private key
        priv_key = load_client_rsa_key(self.client_name, public=False)

        hashed = SHA256.new(message.encode())
        key = RSA.import_key(priv_key)
        signature = pkcs1_15.new(key).sign(hashed)
        return Auth(message, signature.hex())

    def register(self):
        '''Register with the server.'''

        # Load the public key
        pub_key = load_client_rsa_key(self.client_name)

        # Create a registration job
        auth = self.sign_with_priv_key()
        job = RegisterClientJob(
            self.server_address, self.client_name, pub_key, auth)

        # Submit the job
        _resp = job.submit()

        print(_resp)

    def checkin(self):
        '''Tell the server that we are active.'''

        # Create a checkin job
        auth = self.sign_with_priv_key()
        job = CheckinClientJob(
            self.server_address, self.client_name, self.targets, auth)

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

    def send_chunk(self, chunk):
        '''Send a chunk to targets.'''

        # Send jobs to online targets

        # Queue jobs for offline_targets

    def calculate_chunks(self, filename):
        '''Calculate chunks for a changed file.'''


    def sync_target(self, target_name):
        '''Ask server for target's tree so we know what to send.'''

        auth = self.sign_with_priv_key()
        job = GetTreeJob(
            self.server_address, self.client_name, target_name, auth)

    def list_jobs(self):
        '''Print out a list of all jobs this client has.'''
        print('Jobs: ', json.dumps(self.jobs, indent=2))
        print('Defered: ', json.dumps(self.defered_jobs, indent=2))

    def dummy_jobs(self, num=10):
        '''Add dummy test jobs.'''

        job = BatchJob(self.server_address)
        for _ii in range(num):
            auth = self.sign_with_priv_key()
            job.addjob(CheckinClientJob(
                self.server_address, self.client_name, self.targets, auth))
        resp = job.submit()

        json_data = json.loads(resp.text)
        print(json_data)


if __name__ == '__main__':

    client = Client(client_name='client_tester')

    # # Try registering
    # client.register()
    #
    # Try checking in
    client.checkin()

    # # Checkout job queues
    # client.list_jobs()

    # # Try sending a batch job
    # client.dummy_jobs()
