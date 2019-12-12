'''Endpoints to interact with server.'''

import falcon # pylint: disable=E0401
import jsons # pylint: disable=E0401

from backupinator import Server
from backupinator.job import * # allow all job types

# Make an instance of the server to pass to resource objects
SERVER = Server()

class ProcessJob:
    '''Generic handling of Job.'''

    def on_post(self, req, resp):
        '''Ask the server to process a job.'''

        # Get data from request
        data = req.media

        # Deserialize the job object
        job = jsons.load(data, globals()[data['job_type']])

        # Send to job handler and get response
        msg = SERVER.job_handler(job)

        # Send back response
        resp.media = msg


API = falcon.API()
API.add_route('/process_job', ProcessJob())
