'''Authentication class.'''

class Auth:
    '''Abstract away details for authentication.'''

    def __init__(self, message, hex_signature):
        self.message = message
        self.hex_signature = hex_signature
