'''Endpoints to interact with server.'''

import falcon # pylint: disable=E0401

from backupinator import Server, Job

# Make an instance of the server to pass to resource objects
SERVER = Server()

class ProcessJob:
    '''Generic handling of Job.'''

    def on_post(self, req, resp):
        '''Ask the server to process a job.'''

        # Get data from request
        data = req.media

        # Construct a job object
        job = Job(data)

        # Send to job handler and get response
        msg = SERVER.job_handler(job)

        # Send back response
        resp.media = msg


API = falcon.API()
API.add_route('/process_job', ProcessJob())
